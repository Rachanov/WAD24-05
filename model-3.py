import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model
from torch.utils.data import Dataset, random_split
import numpy as np
from torch.utils.data.dataloader import DataLoader
from concurrent.futures import ThreadPoolExecutor
from functools import partial

class SQuADDataset(Dataset):
    def __init__(self, dataset, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples = []
        
        # Batch process examples for speed
        self._batch_process_examples(dataset)
    
    def _batch_process_examples(self, dataset, batch_size=32):
        # Prepare all texts in batches for faster processing
        contexts = []
        questions = []
        answers = []
        
        for example in dataset:
            contexts.append(example['context'])
            questions.append(example['question'])
            answers.append(example['answers']['text'][0] if example['answers']['text'] else "")
            
            if len(contexts) == batch_size:
                self._process_batch(contexts, questions, answers)
                contexts, questions, answers = [], [], []
        
        # Process remaining examples
        if contexts:
            self._process_batch(contexts, questions, answers)
    
    def _process_batch(self, contexts, questions, answers):
        # Create prompts for the batch
        prompts = [
            f"Context: {c}\nQuestion: {q}\nAnswer: {a}"
            for c, q, a in zip(contexts, questions, answers)
        ]
        
        # Batch tokenization
        encodings = self.tokenizer(
            prompts,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Store processed examples
        for i in range(len(prompts)):
            self.examples.append({
                'input_ids': encodings['input_ids'][i],
                'attention_mask': encodings['attention_mask'][i],
                'labels': encodings['input_ids'][i].clone()
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return {
            'input_ids': self.examples[idx]['input_ids'],
            'attention_mask': self.examples[idx]['attention_mask'],
            'labels': self.examples[idx]['labels']
        }

def prepare_model():
    # Optimize model loading and initialization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3.2-3B",
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3.2-3B",
        trust_remote_code=True,
        padding_side="left",
        truncation_side="left",
    )
    tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer

def prepare_lora_config():
    # Optimize LoRA for faster training
    lora_config = LoraConfig(
        r=4,  # Keep rank small for speed
        lora_alpha=32,
        lora_dropout=0.1,
        bias="none",
        target_modules=["q_proj", "v_proj"],
        task_type="CAUSAL_LM",
        inference_mode=False,
    )
    return lora_config

def load_and_prepare_data(tokenizer):
    # Load dataset
    full_dataset = load_dataset("squad", split="train[:1000]")
    
    # Process dataset
    processed_dataset = SQuADDataset(full_dataset, tokenizer)
    
    # Split dataset
    train_size = int(0.9 * len(processed_dataset))
    eval_size = len(processed_dataset) - train_size
    
    return random_split(
        processed_dataset, 
        [train_size, eval_size],
        generator=torch.Generator().manual_seed(42)
    )

class FastTrainer(Trainer):
    def get_train_dataloader(self) -> DataLoader:
        """
        Override to create a more efficient dataloader
        """
        return DataLoader(
            self.train_dataset,
            batch_size=self.args.per_device_train_batch_size,
            shuffle=True,
            num_workers=4,  # Parallel data loading
            pin_memory=True,  # Faster data transfer to GPU
            drop_last=True,  # Slightly faster training
        )

def main():
    try:
        # Enable tensor cores for faster training
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        
        # Set number of threads for CPU operations
        torch.set_num_threads(8)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        
        from huggingface_hub import login
        login(token="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")
        
        print("Preparing model and tokenizer...")
        model, tokenizer = prepare_model()
        
        print("Preparing LoRA configuration...")
        lora_config = prepare_lora_config()
        
        print("Loading and preparing dataset...")
        train_dataset, eval_dataset = load_and_prepare_data(tokenizer)
        print(f"Train size: {len(train_dataset)}, Eval size: {len(eval_dataset)}")
        
        print("Converting to PEFT model...")
        peft_model = get_peft_model(model, lora_config)

        print("Starting training...")
        training_args = TrainingArguments(
            output_dir="./results",
            per_device_train_batch_size=16,  # Increased batch size
            per_device_eval_batch_size=32,   # Larger eval batch size
            gradient_accumulation_steps=2,    # Reduced for speed
            learning_rate=2e-4,
            num_train_epochs=3,
            logging_dir="./logs",
            logging_steps=10,
            save_strategy="epoch",           # Save less frequently
            evaluation_strategy="epoch",     # Evaluate less frequently
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            # Speed optimizations
            fp16=True,                      # Use FP16 for faster training
            dataloader_num_workers=4,       # Parallel data loading
            dataloader_pin_memory=True,     # Faster data transfer to GPU
            optim="adamw_torch",           # Fast optimizer
            bf16=False,                     # Use FP16 instead of BF16
            gradient_checkpointing=False,   # Disable for speed
            report_to=None,                # Disable wandb/tensorboard for speed
        )
        
        trainer = FastTrainer(
            model=peft_model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
        )
        
        trainer.train()
        print("Training completed successfully!")
        
        # Save the fine-tuned model
        peft_model.save_pretrained("./fine_tuned_model")
        print("Model saved to ./fine_tuned_model")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()