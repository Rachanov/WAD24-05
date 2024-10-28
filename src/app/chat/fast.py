from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import json

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # NextJS default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and data
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Load dataset
with open('src/app/chat/fineTuning1.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

questions = [item["question"] for item in dataset]
vectorizer = TfidfVectorizer()
vectorizer.fit(questions)

class ChatMessage(BaseModel):
    message: str

def get_most_similar_question(user_input: str) -> str:
    user_input_vec = vectorizer.transform([user_input])
    similarities = (user_input_vec * vectorizer.transform(questions).T).toarray()
    best_match_idx = similarities.argmax()
    return dataset[best_match_idx]["answer"]

@app.post("/chat")
async def chat(message: ChatMessage):
    user_input = message.message
    
    # Get response from custom dataset
    answer_from_data = get_most_similar_question(user_input)
    
    if answer_from_data:
        return {"response": answer_from_data}
    else:
        # Fallback to DialoGPT
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = model.generate(
            new_user_input_ids, 
            max_length=1000, 
            pad_token_id=tokenizer.eos_token_id
        )
        response_text = tokenizer.decode(
            chat_history_ids[:, new_user_input_ids.shape[-1]:][0], 
            skip_special_tokens=True
        )
        return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)