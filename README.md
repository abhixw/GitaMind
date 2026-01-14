🕉️ Bhagavad Gita RAG Chatbot

LangGraph-powered Conversational AI grounded in the Bhagavad Gita

An intelligent chat-based AI assistant that provides accurate, grounded, and explainable answers from the Bhagavad Gita (English – TTD Edition) using:

Retrieval-Augmented Generation (RAG)

LangGraph conversational orchestration

Long-term chat memory

Intent-aware routing

All interactions happen through a single chat interface — just like ChatGPT — but every answer is faithful to the Bhagavad Gita.

🌟 What Makes This Unique

Unlike normal chatbots, this system:

✔ Only answers from the Bhagavad Gita
✔ Refuses to hallucinate
✔ Tracks conversation context
✔ Detects user intent
✔ Routes requests through different AI pipelines

Everything happens automatically inside the chatbot.

🧠 What the Agent Can Do

The chatbot understands your intent and switches modes automatically:

You say	The agent does
“What is karma yoga?”	📖 RAG question answering
“I feel anxious”	💭 Emotion-based guidance
“I am a student”	🎓 Life-phase guidance
“Give me today’s verse”	🌅 Daily verse
“Give me another verse”	🎲 Random verse
“Compare duty and desire”	⚖️ Dual-RAG comparison

No buttons.
No modes.
Just natural conversation.

🧬 System Architecture
User → Streamlit Chat UI
       ↓
FastAPI Backend
       ↓
LangGraph Agent
       ↓
Intent Router
   ├─ RAG Question Engine
   ├─ Emotion Engine
   ├─ Life-Phase Engine
   └─ Verse Engine
       ↓
Qdrant Vector DB (Bhagavad Gita)
       ↓
Groq LLM (LLaMA-3.1-8B)

🛠️ Tech Stack
AI & Backend

Python

FastAPI

LangChain

LangGraph

Groq LLM (LLaMA-3.1-8B)

HuggingFace Embeddings

Qdrant Vector Database

Frontend

Streamlit

Chat UI

Pillow (images)

Knowledge Base

Bhagavad Gita – English (TTD Edition)

Chunked → Embedded → Stored in Qdrant

📂 Project Structure
rag/
│
├── assets/
│   └── krishna_arjuna.jpeg
│
├── index.py
├── rag_engine.py
├── langgraph_agent.py
├── backend.py
├── app.py
│
├── .env
├── requirements.txt
└── README.md

⚙️ Setup: 
1️⃣ Create Environment
python -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies:
pip install -r requirements.txt

3️⃣ Start Qdrant:
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant


Dashboard:

http://localhost:6333/dashboard

4️⃣ Add .env:
GROQ_API_KEY=your_groq_key
QDRANT_URL=http://localhost:6333

5️⃣ Index the Gita:
python index.py

6️⃣ Start Backend:
python -m uvicorn backend:app --reload

7️⃣ Start Chat UI:
streamlit run app.py



👨‍💻 Author

Abhinav Shrimali
Building intelligent, explainable AI systems with RAG, LangGraph, and LLMs.
