from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_groq import ChatGroq
import os
import datetime
import random

load_dotenv()

COLLECTION_NAME = "bhagavad_gita_ttd1"

embedding_model = HuggingFaceInferenceAPIEmbeddings(
     api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
     model_name="sentence-transformers/all-MiniLM-L6-v2"
 )

vector_db = QdrantVectorStore.from_existing_collection(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name=COLLECTION_NAME,
    embedding=embedding_model,
)

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0
)

# -------------------------
# Core RAG
# -------------------------
def ask_gita(question: str):
    if not isinstance(question, str) or not question.strip():
        return {"answer": "Please ask a valid question.", "confidence": 0, "provenance": []}

    results = vector_db.similarity_search_with_score(question, k=4)

    if not results:
        return {"answer": "No relevant content found in the Bhagavad Gita.", "confidence": 0, "provenance": []}

    context = []
    scores = []
    provenance = []

    for doc, score in results:
        context.append(doc.page_content)
        scores.append(score)
        page = doc.metadata.get("page")
        provenance.append({
            "page": page + 1 if page is not None else "N/A",
            "source": "Bhagavad Gita (TTD)",
            "similarity_score": round(score, 3)
        })

    avg_distance = sum(scores) / len(scores)
    confidence = max(0, min(round((1 - avg_distance) * 100, 2), 100))

    joined_context = "\n\n".join(context)
    system_prompt = f"""
You are a Bhagavad Gita assistant.
Answer ONLY using the provided text.
If the user asks in Hindi, answer in Hindi.
If the user asks in Kannada, answer in Kannada.
If the user asks in Sanskrit, answer in Sanskrit.
If the user asks in English, answer in English.
Always reply in the SAME language as the user's question.

If unclear, say (in the same language):
"I cannot find a clear answer to this in the Bhagavad Gita."

CRITICAL: You MUST structure your answer.
1. List the relevant exact verses first, properly cited (e.g., Chapter X, Verse Y - "exact quote...").
2. Then provide a concise explanation based strictly on those verses.

Context:
{joined_context}
"""

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ])

    return {
        "answer": response.content.strip(),
        "confidence": confidence,
        "provenance": provenance
    }

# -------------------------
# Emotion Mode
# -------------------------
EMOTION_QUERY_MAP = {
    "Anxious": "fear anxiety mental disturbance peace of mind",
    "Angry": "anger wrath desire attachment",
    "Confused": "confusion doubt duty dharma",
    "Sad": "grief sorrow impermanence",
    "Peace": "peace equanimity devotion"
}

def ask_gita_by_emotion(emotion):
    return ask_gita(EMOTION_QUERY_MAP.get(emotion, ""))

# -------------------------
# Life Phase
# -------------------------
LIFE_PHASE_QUERY_MAP = {
    "Student": "learning discipline focus duty",
    "Professional": "work karma yoga responsibility",
    "Leader": "leadership selflessness",
    "Family": "family attachment compassion"
}

def ask_gita_by_life_phase(phase):
    return ask_gita(LIFE_PHASE_QUERY_MAP.get(phase, ""))

# -------------------------
# Daily Verse (same whole day)
# -------------------------
def get_verse_of_the_day():
    today = datetime.date.today().isoformat()
    random.seed(today)

    queries = [
        "duty without attachment",
        "selfless action",
        "peace and equanimity",
        "devotion and surrender",
        "impermanence",
        "control of mind"
    ]

    return ask_gita(random.choice(queries))

# -------------------------
# Random Verse (changes every time)
# -------------------------
def get_random_verse():
    queries = [
        "duty without attachment",
        "selfless action",
        "peace",
        "devotion",
        "impermanence",
        "control of mind",
        "soul immortality",
        "knowledge wisdom",
        "meditation",
        "renunciation",
        "bhakti"
    ]
    return ask_gita(random.choice(queries))
