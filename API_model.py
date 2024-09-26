# from flask import Flask, request, jsonify
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# import torch

# app = Flask(__name__)

# # Load pre-trained chatbot model
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# # Load your custom dataset (assuming it's a list of Q&A)

# import json

# with open('proj/fineTuning1.json', 'r', encoding='utf-8') as f:
#     dataset = json.load(f)

# # for item in dataset:
# #     print(type(item))  # ต้องได้ <class 'dict'> ในแต่ละรายการ
# #     print(item["question"])  # ควรพิมพ์คำถามออกมา

# # dataset = "proj/fineTuning1.json"
# questions = [item["question"] for item in dataset]
# vectorizer = TfidfVectorizer()
# vectorizer.fit(questions)  # ฟิตกับคำถาม

# def get_most_similar_question(user_input):
#     user_input_vec = vectorizer.transform([user_input])
#     similarities = (user_input_vec * vectorizer.transform(questions).T).toarray()
#     best_match_idx = similarities.argmax()
#     return dataset[best_match_idx]["answer"]

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get('message')  # รับข้อมูลจาก request
#     if not user_input:
#         return jsonify({'error': 'No message received'}), 400  # ถ้าไม่มี message ส่งกลับ 400

#     # Find the best answer from the custom dataset
#     answer_from_data = get_most_similar_question(user_input)
    
#     if answer_from_data:
#         return jsonify({'response': answer_from_data})
#     else:
#         # ใช้โมเดลในการสร้างข้อความตอบกลับ
#         new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
#         chat_history_ids = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
#         response_text = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
#         return jsonify({'response': response_text})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# -----------------------------------------------------------------------
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# import torch

# # Load pre-trained chatbot model
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# # Load your custom dataset (assuming it's a list of Q&A)
# import json

# with open('proj/fineTuning1.json', 'r', encoding='utf-8') as f:
#     dataset = json.load(f)

# # Create a TF-IDF model for your dataset
# questions = [item["question"] for item in dataset]
# vectorizer = TfidfVectorizer()
# vectorizer.fit(questions)  # ฟิตกับคำถาม

# def get_most_similar_question(user_input):
#     user_input_vec = vectorizer.transform([user_input])  # ใช้ transform ที่นี่
#     similarities = (user_input_vec * vectorizer.transform(questions).T).toarray()
#     best_match_idx = similarities.argmax()
#     return dataset[best_match_idx]["answer"]

# # Chat loop
# for step in range(5):
#     user_input = input(">> User: ")
    
#     # Find the best answer from the custom dataset
#     answer_from_data = get_most_similar_question(user_input)
    
#     if answer_from_data:
#         print("Data-based Answer: {}".format(answer_from_data))
#     else:
#         # Use the model to generate a response if no good match is found
#         new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
#         bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
#         chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
#         print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))


from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import json

app = Flask(__name__)

# Load pre-trained chatbot model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Load your custom dataset (assuming it's a list of Q&A)
with open('proj/fineTuning1.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

questions = [item["question"] for item in dataset]
vectorizer = TfidfVectorizer()
vectorizer.fit(questions)

def get_most_similar_question(user_input):
    user_input_vec = vectorizer.transform([user_input])
    similarities = (user_input_vec * vectorizer.transform(questions).T).toarray()
    best_match_idx = similarities.argmax()
    return dataset[best_match_idx]["answer"]

@app.route('/')
def index():
    return render_template('chat.html')  # ส่งไฟล์ HTML กลับไป

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    # Find the best answer from the custom dataset
    answer_from_data = get_most_similar_question(user_input)
    
    if answer_from_data:
        return jsonify({'response': answer_from_data})
    else:
        # Use the model to generate a response if no good match is found
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response_text = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
