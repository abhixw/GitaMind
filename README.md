Bhagavad Gita RAG Assistant 🕉️

A Voice-Enabled AI Chatbot grounded strictly in the Bhagavad Gita.

This project is a Retrieval-Augmented Generation (RAG) based system that answers questions using verses from the Bhagavad Gita. It supports multilingual voice interaction and provides contextual, scripture-aligned responses.

Overview

The Bhagavad Gita RAG Assistant is designed to:

Answer philosophical and practical life questions using authentic verses

Provide verse citations (Chapter and Verse)

Support multilingual voice input and output

Offer emotional guidance grounded in scripture

Deliver a daily verse for reflection

The system ensures that responses are generated only from indexed Gita content rather than free-form hallucinated outputs.

Architecture

The system follows a Retrieval-Augmented Generation pipeline:

User Query (Text or Voice)

Speech-to-Text (Whisper)

Embedding Generation

Vector Search (Qdrant)

Context Retrieval (Relevant Verses)

LLM Response Generation (LLaMA 3.1 via Groq)

Text-to-Speech Output (gTTS)

This ensures scripture-grounded answers with citation support.

Core Features
1. Scripture-Based Question Answering

Retrieves relevant verses from the Bhagavad Gita

Generates contextual explanations

Always provides chapter and verse references

Example:

"What does the Gita say about anger?"
Returns relevant verses such as Chapter 2, Verse 62–63.

2. Voice Interaction

Speak your question using your microphone

Whisper converts speech to text

Response is spoken back using gTTS

Supports multilingual speech

3. Multilingual Support

Supports:

English

Hindi

Kannada

Sanskrit

The assistant detects language context and responds accordingly.

4. Emotion-Based Guidance

Users can express emotional states such as:

"I am confused"

"I feel angry"

"I feel hopeless"

The assistant retrieves verses aligned with that emotional state and provides context-based interpretation.

5. Verse of the Day

Random or curated daily verse

Includes Sanskrit shloka

Transliteration

Translation

Brief explanation

Tech Stack

Frontend

Streamlit

LLM

LLaMA 3.1 via Groq API

Vector Database

Qdrant

Orchestration

LangGraph

Voice Stack

Whisper (Speech-to-Text)

gTTS (Text-to-Speech)

Embeddings

Compatible embedding model (e.g., OpenAI/Groq-supported embedding model)

Project Structure (Suggested)
Bhagavad-Gita-RAG/
│
├── app.py
├── core/
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── voice.py
│   ├── verse_of_day.py
│   └── emotion_mapper.py
│
├── data/
│   └── bhagavad_gita.json
│
├── requirements.txt
├── .env
└── README.md

Setup Instructions
1. Clone Repository
git clone https://github.com/your-username/bhagavad-gita-rag.git
cd bhagavad-gita-rag

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file:

GROQ_API_KEY=your_groq_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key

Running the App
streamlit run app.py


Default:

http://localhost:8501
