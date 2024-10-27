import os
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments,
    DataCollatorForSeq2Seq
)

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def load_data(data_path: str, tokenizer):
    """Load and prepare data for training"""
    df = pd.read_json(data_path)

    # Combine question and answer for the chatbot format
    df['formatted'] = df.apply(
        lambda row: f"<human>{row['question']}<sep><assistant>{row['answer']}<eos>", axis=1
    )

    train_texts, val_texts = train_test_split(df['formatted'].tolist(), test_size=0.1)

    # Tokenize with decoder_input_ids
    train_encodings = tokenizer(train_texts, padding=True, truncation=True)
    val_encodings = tokenizer(val_texts, padding=True, truncation=True)

    # Add labels and decoder_input_ids
    train_encodings['labels'] = train_encodings['input_ids']
    val_encodings['labels'] = val_encodings['input_ids']

    # Convert to Hugging Face Dataset
    train_dataset = Dataset.from_dict(train_encodings)
    val_dataset = Dataset.from_dict(val_encodings)

    return train_dataset, val_dataset


def fine_tune_model(data_path: str, model_name="google/mt5-small", output_dir="./mt5-fine"):
    """Fine-tune the model with prepared data"""
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Load dataset
    train_dataset, val_dataset = load_data(data_path, tokenizer)

    # Data collator for padding
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir='./logs',
        save_total_limit=2,
        load_best_model_at_end=True,
        remove_unused_columns=False
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator
    )

    # Train the model
    trainer.train()

    # Save the fine-tuned model and tokenizer
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)


def chatbot_response(input_text, model_path="./fine_tuned_model"):
    """Generate a chatbot response using the fine-tuned model"""
    # Load the fine-tuned model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    # Tokenize the input
    inputs = tokenizer(input_text, return_tensors="pt", padding=True)

    # Generate the response; model.generate will handle decoder_input_ids automatically
    outputs = model.generate(
        inputs["input_ids"],
        max_length=100,
        num_beams=5,
        early_stopping=True
    )

    # Decode and return the response
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage:
# Fine-tune the model (ensure your data path is correct)
data_path = "./fineTuning1.json"  # Update with the correct path
fine_tune_model(data_path)

# Chatbot interaction
user_input = "What is an agricultural drone?"
response = chatbot_response(user_input)
print("Chatbot:", response)
