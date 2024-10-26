import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model

def prepare_model():
    # กำหนดค่า configuration สำหรับ quantization
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # กำหนดค่า configuration สำหรับ quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )
    
    # โหลด base model
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3.2-3B",
        quantization_config=bnb_config,
        device_map={"": device},  # แก้ไขตรงนี้
        trust_remote_code=True,
    )
    
    # โหลด tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3.2-3B",
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

def prepare_lora_config():
    # กำหนดค่า configuration สำหรับ LoRA
    lora_config = LoraConfig(
        r=8,  # rank
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    return lora_config

def prepare_training_dataset(data_path):
    """
    เตรียม dataset สำหรับการ fine-tuning
    data_path: path ไปยังไฟล์ข้อมูลของคุณ (ควรอยู่ในรูปแบบที่เหมาะสม เช่น CSV หรือ JSON)
    """
    # ตัวอย่างการโหลดข้อมูล - ปรับแต่งตามรูปแบบข้อมูลของคุณ
    dataset = load_dataset('json', data_files=data_path)
    return dataset['train']
    
    # def format_instruction(example):
    #     """
    #     แปลงข้อมูลให้อยู่ในรูปแบบที่เหมาะสมสำหรับการ training
    #     """
    #     return {
    #         'text': f"### Question: {example['question']}\n### Answer: {example['answer']}"
    #     }
    
    # formatted_dataset = dataset.map(format_instruction)
    # return formatted_dataset

def train_model(model, tokenizer, dataset, output_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    def collate_fn(examples):
        inputs = tokenizer([ex['text'] for ex in examples], 
                         padding=True, 
                         truncation=True, 
                         return_tensors="pt")
        # ย้าย inputs ไปยัง device ที่ถูกต้อง
        return {k: v.to(device) for k, v in inputs.items()}

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        learning_rate=2e-5,
        save_strategy="epoch",
        save_total_limit=2,
        save_steps=10,
        logging_steps=10,
        remove_unused_columns=False,
        no_cuda=not torch.cuda.is_available(),
        fp16=False,
        use_cpu=not torch.cuda.is_available(),  # เพิ่มบรรทัดนี้
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=collate_fn,
    )
    
    return trainer

def test_model(model, tokenizer, question):
    prompt = f"### คำถาม: {question}\n### คำตอบ:"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        num_return_sequences=1,
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def main():
    try:
        # Set device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        
        from huggingface_hub import login
        login(token="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")
        
        print("Preparing model and tokenizer...")
        model, tokenizer = prepare_model()
        
        # Move model to correct device
        model = model.to(device)
        
        print("Preparing LoRA configuration...")
        # 2. เตรียม LoRA configuration
        lora_config = prepare_lora_config()
        
        print("Converting to PEFT model...")
        # 3. แปลง model เป็น PEFT model
        model = get_peft_model(model, lora_config)
        
        print("Loading dataset...")
        # 4. เตรียม dataset
        dataset = prepare_training_dataset("./fineTuning1.json")
        print(f"Dataset size: {len(dataset)} examples")
        
        print("Starting training...")
        # 5. Train model
        trainer = train_model(model, tokenizer, dataset, "./llama_agriculture_model")
        
        print("Saving model...")
        # 6. Save trained model
        trainer.save_model("llama-3.1")
        
        print("Testing model...")
        test_question = "โดรนทางการเกษตรคืออะไร"
        response = test_model(model, tokenizer, test_question)
        print(f"คำถาม: {test_question}")
        print(f"คำตอบ: {response}")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")
        raise

if __name__ == "__main__":
    main()