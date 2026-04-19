import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from .langgraph_agent import agent

app = FastAPI(title="Bhagavad Gita Agentic API")

class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    input_state = {"messages": req.messages}
    result_state = agent.invoke(input_state)
    return result_state.get("reply", {})
