import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
# เพิ่ม environment variable สำหรับ PyTorch CUDA allocation
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments, 
    DataCollatorForSeq2Seq
)
import numpy as np
import torch

def load_data(data_path: str, tokenizer):
    """โหลดและเตรียมข้อมูลสำหรับการ fine-tuning"""
    df = pd.read_json(data_path)
    
    # Convert float values to strings and handle NaN values
    df['question'] = df['question'].apply(lambda x: str(x) if pd.notnull(x) else '')
    df['answer'] = df['answer'].apply(lambda x: str(x) if pd.notnull(x) else '')
    
    # แบ่งข้อมูลสำหรับ training และ validation
    train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)

    def preprocess_function(examples):
        """แปลงข้อมูลให้อยู่ในรูปแบบที่เหมาะสม"""
        questions = examples['question']
        answers = examples['answer']
        
        if isinstance(questions, str):
            questions = [questions]
        if isinstance(answers, str):
            answers = [answers]

        # Convert any non-string elements to strings
        questions = [str(q) for q in questions]
        answers = [str(a) for a in answers]

        # Tokenize inputs (ลดความยาว sequence ลง)
        model_inputs = tokenizer(
            questions,
            max_length=128,  # ลดลงจาก 256
            padding="max_length",
            truncation=True
        )

        # Tokenize targets (ลดความยาว sequence ลง)
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(
                answers,
                max_length=128,  # ลดลงจาก 512
                padding="max_length",
                truncation=True
            )

        model_inputs['labels'] = labels['input_ids']
        return model_inputs

    # Check and clean data before creating datasets
    train_questions = [str(q) for q in train_df['question'].tolist()]
    train_answers = [str(a) for a in train_df['answer'].tolist()]
    val_questions = [str(q) for q in val_df['question'].tolist()]
    val_answers = [str(a) for a in val_df['answer'].tolist()]

    # สร้าง datasets
    train_dataset = Dataset.from_dict({
        'question': train_questions,
        'answer': train_answers
    })
    
    val_dataset = Dataset.from_dict({
        'question': val_questions,
        'answer': val_answers
    })

    # แปลงข้อมูล (ลด batch_size ลง)
    train_dataset = train_dataset.map(
        preprocess_function,
        batched=True,
        batch_size=4,  # ลดลงจาก 8
        remove_columns=train_dataset.column_names
    )
    
    val_dataset = val_dataset.map(
        preprocess_function,
        batched=True,
        batch_size=4,  # ลดลงจาก 8
        remove_columns=val_dataset.column_names
    )

    return train_dataset, val_dataset

def fine_tune_model(
    data_path: str, 
    model_name="google/mt5-small",
    output_dir="./fine_tuned_model"
):
    """ทำ Fine-tuning โมเดล"""
    
    # Clear CUDA cache
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # สร้าง tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        model_max_length=128,  # ลดลงจาก 512
        legacy=False
    )
    
    try:
        # โหลดข้อมูล
        train_dataset, val_dataset = load_data(data_path, tokenizer)
        
        # โหลดโมเดล
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            # เพิ่ม gradient checkpointing เพื่อประหยัด memory
            use_cache=False
        )
        
        # Enable gradient checkpointing
        model.gradient_checkpointing_enable()
        
        # สร้าง data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=tokenizer,
            model=model,
            padding="max_length",
            max_length=128  # ลดลงจาก 512
        )

        # กำหนดค่า training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="steps",
            eval_steps=100,
            save_strategy="steps",
            save_steps=100,
            learning_rate=2e-5,
            per_device_train_batch_size=2,  # ลดลงจาก 4
            per_device_eval_batch_size=2,   # ลดลงจาก 4
            num_train_epochs=5,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            save_total_limit=2,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            # เพิ่ม gradient accumulation เพื่อชดเชย batch size ที่ลดลง
            gradient_accumulation_steps=4,  # เพิ่มจาก 2
            # เพิ่ม mixed precision training
            fp16=True,
            optim="adamw_torch_fused"  # ใช้ optimizer ที่ประหยัด memory
        )

        # สร้าง trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=tokenizer,
            data_collator=data_collator,
        )

        # เริ่ม training
        trainer.train()
        
        # บันทึกโมเดล
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        print(f"บันทึกโมเดลไว้ที่ {output_dir}")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")
        # Print the first few rows of the data for debugging
        df = pd.read_json(data_path)
        print("\nตัวอย่างข้อมูล:")
        print(df.head())
        print("\nประเภทข้อมูล:")
        print(df.dtypes)

if __name__ == "__main__":
    data_path = "./fineTuning1.json"
    fine_tune_model(data_path)