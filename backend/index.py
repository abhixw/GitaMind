from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

load_dotenv()

# -------------------------
# CONFIG
# -------------------------
PDF_PATH = Path(__file__).parent / "Bhagavad-Gita.pdf"
COLLECTION_NAME = "bhagavad_gita_ttd1"

if not PDF_PATH.exists():
    raise RuntimeError(f"❌ PDF not found: {PDF_PATH}")

print(f"📖 Loading Bhagavad Gita PDF: {PDF_PATH.name}")

# -------------------------
# Load PDF
# -------------------------
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

print(f"📄 Total pages loaded: {len(docs)}")

# -------------------------
# Chunking (optimized for scripture)
# -------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=120
)

chunks = text_splitter.split_documents(docs)

# Add metadata
for chunk in chunks:
    chunk.metadata["source"] = "Bhagavad Gita (English)"
    chunk.metadata["book"] = "Bhagavad Gita"
    chunk.metadata["file"] = PDF_PATH.name

print(f"✂️ Total chunks created: {len(chunks)}")

# -------------------------
# Embeddings
# -------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------
# Store in Qdrant
# -------------------------
QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name=COLLECTION_NAME,
    force_recreate=True
)

print("✅ Bhagavad Gita fully indexed into Qdrant.")
print(f"📚 Collection: {COLLECTION_NAME}")
