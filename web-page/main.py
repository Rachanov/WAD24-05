import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import uvicorn

# สร้าง global variables สำหรับเก็บ model และ tokenizer
global_model = None
global_tokenizer = None

app = FastAPI(title="LLaMA Chat API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/web-page/static", StaticFiles(directory="web-page/static"), name="static")

def initialize_model():
    global global_model, global_tokenizer
    if global_model is None or global_tokenizer is None:
        try:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"Using device: {device}")
            
            model = AutoModelForCausalLM.from_pretrained(
                "llama-3.1",
                device_map={"": device},
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            )
            
            tokenizer = AutoTokenizer.from_pretrained(
                "meta-llama/Llama-3.2-3B",
                trust_remote_code=True
            )
            
            global_model = model.to(device)
            global_tokenizer = tokenizer
            print("Model and tokenizer loaded successfully")
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

class ChatRequest(BaseModel):
    message: str
    max_length: int = 512
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    error: str = None

@app.on_event("startup")
async def startup_event():
    initialize_model()

@app.get("/")
async def read_root():
    return FileResponse("web-page/static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        if global_model is None or global_tokenizer is None:
            raise HTTPException(status_code=500, detail="Model not initialized")
            
        prompt = f"### คำถาม: {request.message}\n### คำตอบ:"
        inputs = global_tokenizer(prompt, return_tensors="pt").to(global_model.device)
        
        with torch.no_grad():
            outputs = global_model.generate(
                **inputs,
                max_new_tokens=request.max_length,
                temperature=request.temperature,
                num_return_sequences=1,
                do_sample=True,
                top_p=0.9,
                pad_token_id=global_tokenizer.eos_token_id,
            )
        
        response = global_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return ChatResponse(response=response)
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return ChatResponse(
            response="",
            status="error",
            error=str(e)
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)