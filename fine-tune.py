import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import json
import pandas as pd
from sklearn.model_selection import train_test_split
import logging
from typing import Dict, List, Tuple
from pythainlp.tokenize import word_tokenize

class ThaiChatbotTrainer:
    def __init__(
        self,
        model_name="airesearch/wangchanberta-base-att-spm-uncased",  # เปลี่ยนเป็น WangchanBERTa
        output_dir="./fine_tuned_model"
    ):
        self.model_name = model_name
        self.output_dir = output_dir
        self.setup_logging()
        self.setup_model_and_tokenizer()

    def setup_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def analyze_dataset_stats(self, json_file: str) -> dict:
        """Analyze dataset statistics including average lengths and token counts"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            question_lengths = []
            answer_lengths = []
            question_token_counts = []
            answer_token_counts = []
            
            for item in data:
                if isinstance(item, dict):
                    question = item.get('question', '')
                    answer = item.get('answer', '')
                    
                    # Character lengths
                    question_lengths.append(len(question))
                    answer_lengths.append(len(answer))
                    
                    # Token counts using PyThaiNLP
                    question_tokens = word_tokenize(question, engine="newmm")
                    answer_tokens = word_tokenize(answer, engine="newmm")
                    question_token_counts.append(len(question_tokens))
                    answer_token_counts.append(len(answer_tokens))
            
            stats = {
                'total_examples': len(data),
                'avg_question_length': sum(question_lengths) / len(question_lengths) if question_lengths else 0,
                'avg_answer_length': sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0,
                'avg_question_tokens': sum(question_token_counts) / len(question_token_counts) if question_token_counts else 0,
                'avg_answer_tokens': sum(answer_token_counts) / len(answer_token_counts) if answer_token_counts else 0,
                'max_question_length': max(question_lengths) if question_lengths else 0,
                'max_answer_length': max(answer_lengths) if answer_lengths else 0,
                'max_question_tokens': max(question_token_counts) if question_token_counts else 0,
                'max_answer_tokens': max(answer_token_counts) if answer_token_counts else 0
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error analyzing dataset: {str(e)}")
            raise
    
    def setup_model_and_tokenizer(self):
        """Initialize model and tokenizer with proper configuration for Thai language"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                use_fast=False,
                model_max_length=512
            )
            
            # เพิ่ม special tokens สำหรับการ fine-tune chatbot
            special_tokens = {
                "pad_token": "<pad>",
                "sep_token": "<sep>",
                "eos_token": "<eos>",
                "additional_special_tokens": ["<human>", "<assistant>"]
            }
            self.tokenizer.add_special_tokens(special_tokens)
            
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.model.resize_token_embeddings(len(self.tokenizer))
            
            self.logger.info("Model and tokenizer initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing model/tokenizer: {str(e)}")
            raise

    def preprocess_thai_text(self, text: str) -> str:
        """Preprocess Thai text using PyThaiNLP"""
        # ทำการ word tokenize ด้วย PyThaiNLP
        tokens = word_tokenize(text, engine="newmm")
        return " ".join(tokens)

    def format_conversation(self, question: str, answer: str) -> str:
        """Format a single conversation pair with special tokens and preprocessing"""
        # Preprocess both question and answer
        processed_question = self.preprocess_thai_text(question)
        processed_answer = self.preprocess_thai_text(answer)
        return f"<human>{processed_question}<sep><assistant>{processed_answer}<eos>"

    def prepare_data(self, json_file: str) -> Tuple[Dataset, Dataset]:
        """Prepare and validate training data"""
        try:
            # Load and validate data
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list of conversation pairs")
            
            # Process conversations with Thai text preprocessing
            conversations = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                    
                question = item.get('question', '')
                answer = item.get('answer', '')
                
                if question and answer:
                    formatted_conv = self.format_conversation(question, answer)
                    conversations.append(formatted_conv)
            
            if not conversations:
                raise ValueError("No valid conversations found in data")
            
            # Split data
            train_texts, val_texts = train_test_split(
                conversations,
                test_size=0.1,
                random_state=42
            )
            
            # Create datasets
            train_dataset = Dataset.from_dict({"text": train_texts})
            val_dataset = Dataset.from_dict({"text": val_texts})
            
            # Tokenization function optimized for Thai language
            def tokenize_function(examples):
                try:
                    return self.tokenizer(
                        examples["text"],
                        truncation=True,
                        padding="max_length",
                        max_length=512,
                        return_special_tokens_mask=True
                    )
                except Exception as e:
                    self.logger.error(f"Tokenization error: {str(e)}")
                    raise
            
            # Tokenize datasets
            train_encoded = train_dataset.map(
                tokenize_function,
                remove_columns=["text"],
                num_proc=4
            )
            val_encoded = val_dataset.map(
                tokenize_function,
                remove_columns=["text"],
                num_proc=4
            )
            
            self.logger.info(f"Prepared {len(train_encoded)} training examples")
            self.logger.info(f"Prepared {len(val_encoded)} validation examples")
            
            return train_encoded, val_encoded
            
        except Exception as e:
            self.logger.error(f"Error in data preparation: {str(e)}")
            raise

    def train(
        self,
        train_dataset: Dataset,
        val_dataset: Dataset,
        training_args: TrainingArguments = None
    ) -> bool:
        """Execute the training process with error handling"""
        try:
            if training_args is None:
                training_args = TrainingArguments(
                    output_dir="./fine_tuned_model",
                    num_train_epochs=3,
                    per_device_train_batch_size=2,  # ลดลงเพื่อประหยัด VRAM
                    per_device_eval_batch_size=2,
                    gradient_accumulation_steps=8,  # เพิ่มขึ้นเพื่อชดเชย batch size ที่เล็กลง
                    warmup_ratio=0.1,
                    weight_decay=0.01,
                    logging_dir="./logs",
                    logging_steps=10,
                    evaluation_strategy="steps",
                    eval_steps=50,
                    save_strategy="steps",
                    save_steps=100,
                    load_best_model_at_end=True,
                    save_total_limit=2,  # ลดจำนวน checkpoints ที่เก็บไว้
                    fp16=True,  # ใช้ mixed precision training
                    gradient_checkpointing=True,  # ช่วยประหยัด VRAM
                    learning_rate=1e-5
                )

            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False
            )

            # Initialize trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                data_collator=data_collator,
            )

            # Training
            self.logger.info("Starting training...")
            trainer.train()
            
            # Save the model
            self.logger.info(f"Saving model to {self.output_dir}")
            trainer.save_model()
            self.tokenizer.save_pretrained(self.output_dir)
            
            return True

        except Exception as e:
            self.logger.error(f"Training error: {str(e)}")
            return False

def main():
    # Initialize trainer
    trainer = ThaiChatbotTrainer()
    
    try:
        stats = trainer.analyze_dataset_stats("fineTuning1.json")
        print("Dataset Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value:.2f}")
        # Prepare data
        train_dataset, val_dataset = trainer.prepare_data("fineTuning1.json")
        
        # Configure training arguments
        training_args = TrainingArguments(
            output_dir="./fine_tuned_model",
            num_train_epochs=3,
            per_device_train_batch_size=2,  # ลดลงเพื่อประหยัด VRAM
            per_device_eval_batch_size=2,
            gradient_accumulation_steps=8,  # เพิ่มขึ้นเพื่อชดเชย batch size ที่เล็กลง
            warmup_ratio=0.1,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            evaluation_strategy="steps",
            eval_steps=50,
            save_strategy="steps",
            save_steps=100,
            load_best_model_at_end=True,
            save_total_limit=2,  # ลดจำนวน checkpoints ที่เก็บไว้
            fp16=True,  # ใช้ mixed precision training
            gradient_checkpointing=True,  # ช่วยประหยัด VRAM
            learning_rate=1e-5
        )
        
        # Execute training
        success = trainer.train(train_dataset, val_dataset, training_args)
        
        if success:
            print("Training completed successfully!")
        else:
            print("Training failed. Check the logs for details.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please check the logs for more details.")

if __name__ == "__main__":
    main()