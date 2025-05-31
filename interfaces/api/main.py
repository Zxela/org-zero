# interfaces/api/main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.director.agent import DirectorAgent

app = FastAPI()
director = DirectorAgent()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = director.handle_user_input(request.message)
    return {"response": response}
