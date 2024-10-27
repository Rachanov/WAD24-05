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
    def __init__(self, model_path="./fine_tuned_model", fallback_model="google/mt5-small"):
        self.model_path = model_path
        self.fallback_model = fallback_model
        self.setup_logging()
        self.load_model_and_tokenizer()

    def setup_logging(self):
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
                
                # Add special tokens if they don't exist
                special_tokens_dict = {
                    'pad_token': '<pad>',
                    'sep_token': '<sep>',
                    'eos_token': '</s>',
                    'bos_token': '<s>',
                    'unk_token': '<unk>',
                    'mask_token': '<mask>',
                    'additional_special_tokens': ['<human>', '<assistant>']
                }
                
                num_added_toks = self.tokenizer.add_special_tokens(special_tokens_dict)
                
                self.model = AutoModelForCausalLM.from_pretrained(self.fallback_model)
                self.model.resize_token_embeddings(len(self.tokenizer))
                self.logger.info(f"Successfully loaded base model and added {num_added_toks} special tokens")
            except Exception as e:
                self.logger.error(f"Critical error loading base model: {str(e)}")
                raise RuntimeError("Could not initialize either fine-tuned or base model")
        
        # Ensure model is in evaluation mode
        self.model.eval()
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.logger.info(f"Model loaded on device: {self.device}")

    def preprocess_input(self, text: str) -> str:
        try:
            tokens = word_tokenize(text, engine="newmm")
            return " ".join(tokens)
        except Exception as e:
            self.logger.warning(f"Error in preprocessing: {str(e)}")
            return text

    def encode_input(self, text: str) -> torch.Tensor:
        """Encode input text to tensor format"""
        try:
            # Format input with special tokens
            formatted_text = f"<human>{text}<sep><assistant>"
            
            # Tokenize with proper padding and attention mask
            encoded = self.tokenizer(
                formatted_text,
                add_special_tokens=True,
                padding='max_length',
                truncation=True,
                max_length=512,
                return_tensors='pt'
            )
            
            # Move tensors to correct device
            encoded = {k: v.to(self.device) for k, v in encoded.items()}
            
            return encoded
            
        except Exception as e:
            self.logger.error(f"Error encoding input: {str(e)}")
            raise

    def generate_response(self, user_input: str, max_new_tokens: int = 50) -> str:
        try:
            processed_input = self.preprocess_input(user_input)
            prompt = f"<human>{processed_input}<sep><assistant>"

            inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(device)
            self.model.to(device)
            input_ids = inputs["input_ids"].to(device)

            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=input_ids,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    num_return_sequences=1,
                    no_repeat_ngram_size=2,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            if response.startswith(processed_input):
                response = response[len(processed_input):].strip()

            return response or "ขออภัย ฉันไม่สามารถสร้างคำตอบที่เหมาะสมได้"
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
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
                print(f"dronejai: {response}")
                
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