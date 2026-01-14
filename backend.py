from fastapi import FastAPI
from pydantic import BaseModel
from langgraph_agent import agent

app = FastAPI(title="Bhagavad Gita LangGraph RAG")

class ChatRequest(BaseModel):
    message: str
    session_id: str

# In-memory chat history
memory = {}

@app.post("/chat")
def chat(req: ChatRequest):
    history = memory.get(req.session_id, [])

    history.append({
        "role": "user",
        "content": req.message
    })

    result = agent.invoke({
        "messages": history
    })

    history.append({
        "role": "assistant",
        "content": result["reply"]
    })

    memory[req.session_id] = history

    return result["reply"]
