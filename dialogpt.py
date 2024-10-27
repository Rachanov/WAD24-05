import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from sentence_transformers import SentenceTransformer, util
from pythainlp.tokenize import word_tokenize
import torch
import json

app = Flask(__name__)

class ImprovedChatbot:
    def __init__(self, model_path="./fine_tuned_model"):
        # Load WangchanBERTa model and tokenizer
        if os.path.exists(model_path):
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                use_fast=True,
                model_max_length=512
            )
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
        else:
            # Fallback to base WangchanBERTa model
            base_model = "microsoft/DialoGPT-small"
            self.tokenizer = AutoTokenizer.from_pretrained(
                base_model,
                use_fast=True,
                model_max_length=512
            )
            self.model = AutoModelForCausalLM.from_pretrained(base_model)
            
            # Add special tokens as defined in fine-tune.py
            special_tokens = {
                "pad_token": "<pad>",
                "sep_token": "<sep>",
                "eos_token": "<eos>",
                "additional_special_tokens": ["<human>", "<assistant>"]
            }
            self.tokenizer.add_special_tokens(special_tokens)
            self.model.resize_token_embeddings(len(self.tokenizer))
        
        self.chat_model = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )
        
        # Load sentence transformer for semantic search
        self.sentence_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Load dataset and prepare embeddings
        self.load_dataset()

    def preprocess_thai_text(self, text: str) -> str:
        """Preprocess Thai text using PyThaiNLP similar to fine-tune.py"""
        tokens = word_tokenize(text, engine="newmm")
        return " ".join(tokens)

    def format_conversation(self, question: str) -> str:
        """Format conversation with special tokens matching fine-tune.py"""
        processed_question = self.preprocess_thai_text(question)
        return f"<human>{processed_question}<sep><assistant>"

    def load_dataset(self):
        with open('fineTuning1.json', 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)
        # Preprocess questions for consistency
        self.questions = [self.preprocess_thai_text(item["question"]) for item in self.dataset]
        self.question_embeddings = self.sentence_model.encode(self.questions, convert_to_tensor=True)

    def get_similar_questions(self, user_input, threshold=0.7):
        # Preprocess input for consistency with dataset
        processed_input = self.preprocess_thai_text(user_input)
        input_embedding = self.sentence_model.encode(processed_input, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(input_embedding, self.question_embeddings)[0]
        
        best_matches = []
        for idx, score in enumerate(cosine_scores):
            if score > threshold:
                best_matches.append({
                    'question': self.questions[idx],
                    'answer': self.dataset[idx]["answer"],
                    'score': score.item()
                })
        
        return sorted(best_matches, key=lambda x: x['score'], reverse=True)

    def generate_response(self, user_input):
        try:
            # Format input with special tokens
            formatted_input = self.format_conversation(user_input)
            
            # First try similar questions from dataset
            similar_questions = self.get_similar_questions(user_input)
            
            if similar_questions and similar_questions[0]['score'] > 0.8:
                return {
                    'response': similar_questions[0]['answer'],
                    'confidence': similar_questions[0]['score'],
                    'source': 'dataset'
                }
            
            # Use fine-tuned model for generation
            model_response = self.chat_model(
                formatted_input,
                max_length=512,  # Match model_max_length from tokenizer
                num_return_sequences=1,
                clean_up_tokenization_spaces=True,
                no_repeat_ngram_size=2,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )[0]['generated_text']
            
            # Clean up response and extract assistant's reply
            response = model_response.split("<assistant>")[-1].split("<eos>")[0].strip()
            
            return {
                'response': response,
                'confidence': 0.7,
                'source': 'fine-tuned_model'
            }
            
        except Exception as e:
            return {
                'response': f'ขออภัย เกิดข้อผิดพลาด: {str(e)}',
                'confidence': 0,
                'source': 'error'
            }

# Initialize chatbot
chatbot = ImprovedChatbot()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()
    
    if not user_input:
        return jsonify({
            'response': 'กรุณาพิมพ์ข้อความค่ะ',
            'confidence': 0
        })

    result = chatbot.generate_response(user_input)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)