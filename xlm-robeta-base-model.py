import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import torch
import logging
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
from typing import Dict, List, Tuple
from pythainlp.tokenize import word_tokenize

class ThaiChatbot:
    def __init__(self, model_path="./fine_tuned_model", fallback_model="xlm-roberta-base"):
        """
        Initialize the chatbot with either fine-tuned model or fallback to base model
        Args:
            model_path: Path to fine-tuned model
            fallback_model: Model to use if fine-tuned model isn't found
        """
        self.model_path = model_path
        self.fallback_model = fallback_model
        self.setup_logging()
        self.load_model_and_tokenizer()

    def setup_logging(self):
        """Initialize logging configuration"""
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('chatbot.log'),
                logging.StreamHandler()
            ]
        )

    def load_model_and_tokenizer(self):
        """Load either fine-tuned model or fall back to base model"""
        try:
            # First try to load fine-tuned model
            self.logger.info(f"Attempting to load fine-tuned model from {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            self.logger.info("Successfully loaded fine-tuned model")
        except Exception as e:
            self.logger.warning(f"Could not load fine-tuned model: {str(e)}")
            self.logger.info(f"Falling back to base model: {self.fallback_model}")
            
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.fallback_model,
                    use_fast=True,
                    model_max_length=512
                )
                
                # Add special tokens
                special_tokens = {
                    "pad_token": "<pad>",
                    "sep_token": "<sep>",
                    "eos_token": "<eos>",
                    "additional_special_tokens": ["<human>", "<assistant>"]
                }
                self.tokenizer.add_special_tokens(special_tokens)
                
                self.model = AutoModelForCausalLM.from_pretrained(self.fallback_model)
                self.model.resize_token_embeddings(len(self.tokenizer))
                self.logger.info("Successfully loaded base model")
            except Exception as e:
                self.logger.error(f"Critical error loading base model: {str(e)}")
                raise RuntimeError("Could not initialize either fine-tuned or base model")
        
        self.model.eval()

    def preprocess_input(self, text: str) -> str:
        """Preprocess input text using PyThaiNLP"""
        try:
            tokens = word_tokenize(text, engine="newmm")
            return " ".join(tokens)
        except Exception as e:
            self.logger.warning(f"Error in preprocessing: {str(e)}")
            return text  # Return original text if preprocessing fails

    def generate_response(self, user_input: str, max_length: int = 100) -> str:
        """
        Generate a response for the given user input
        Args:
            user_input: User's input text
            max_length: Maximum length of generated response
        Returns:
            str: Generated response or error message
        """
        try:
            # Preprocess input
            processed_input = self.preprocess_input(user_input)
            
            # Format input with special tokens
            prompt = f"<human>{processed_input}<sep><assistant>"
            
            # Tokenize
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Check if GPU is available
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(device)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_length=max_length,
                    num_return_sequences=1,
                    no_repeat_ngram_size=2,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up response
            response = response.replace(prompt, "").strip()
            
            if not response:
                return "ขออภัย ฉันไม่สามารถสร้างคำตอบที่เหมาะสมได้ กรุณาลองใหม่อีกครั้ง"
                
            return response
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return "ขออภัย เกิดข้อผิดพลาดในการประมวลผล กรุณาลองใหม่อีกครั้ง"

def main():
    try:
        print("กำลังโหลดแชทบอท...")
        chatbot = ThaiChatbot()
        print("Thai Chatbot พร้อมให้บริการแล้ว! (พิมพ์ 'exit' เพื่อออกจากโปรแกรม)")
        
        while True:
            try:
                user_input = input("\nคุณ: ").strip()
                if not user_input:
                    print("กรุณาพิมพ์ข้อความ")
                    continue
                    
                if user_input.lower() == 'exit':
                    print("ขอบคุณที่ใช้บริการ!")
                    break
                    
                response = chatbot.generate_response(user_input)
                print(f"แชทบอท: {response}")
                
            except KeyboardInterrupt:
                print("\nกำลังปิดโปรแกรม...")
                break
                
            except Exception as e:
                print(f"เกิดข้อผิดพลาด: {str(e)}")
                print("กรุณาลองใหม่อีกครั้ง")
                
    except Exception as e:
        print(f"เกิดข้อผิดพลาดร้ายแรง: {str(e)}")
        print("ไม่สามารถเริ่มต้นแชทบอทได้")

if __name__ == "__main__":
    main()