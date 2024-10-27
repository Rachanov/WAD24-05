# api.py
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    context: str = ""  # เพิ่มฟิลด์สำหรับบริบทการสนทนา

def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModelForCausalLM.from_pretrained(
        "./llama-3.2",
        device_map={"": device},
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3.2-1B",
        trust_remote_code=True
    )
    return model, tokenizer

model, tokenizer = load_model()

def create_prompt(message: str, context: str = "") -> str:
    """สร้าง prompt ที่มีโครงสร้างชัดเจนและมีบริบท"""
    system_prompt = """คุณคือผู้ช่วยที่เป็นมิตรและมีความรู้รอบด้าน สามารถตอบคำถามได้อย่างแม่นยำ เน้นไปทางด้านการเกษตรและโดรนทางการเกษตรโดยเฉพาะ ซึ่งจะคำตอบที่เป็นประโยชน์และเข้าใจง่าย"""
    
    if context:
        return f"""### บริบท: {system_prompt}
    ### ประวัติการสนทนา: {context}
    ### คำถามปัจจุบัน: {message}
    ### คำตอบ:"""
    else:
        return f"""### บริบท: {system_prompt}
        ### คำถาม: {message}
        ### คำตอบ:"""

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # สร้าง prompt ที่มีโครงสร้างดีขึ้น
        prompt = create_prompt(request.message, request.context)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # ปรับค่า parameters สำหรับการ generate
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,  # เพิ่มความยาวคำตอบ
            temperature=0.7,     # เพิ่มความหลากหลาย
            num_return_sequences=1,
            do_sample=True,
            top_p=0.92,
            top_k=50,
            repetition_penalty=1.1,
            no_repeat_ngram_size=3,
            early_stopping=True
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # ตัดเฉพาะส่วนคำตอบ
        response = response.split("### คำตอบ:")[-1].strip()
        
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)