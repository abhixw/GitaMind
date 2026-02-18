# Bhagavad Gita RAG Assistant 🕉️

A Voice-Enabled AI Chatbot grounded strictly in the Bhagavad Gita.

This project implements a Retrieval-Augmented Generation (RAG) system that answers user questions using verses from the Bhagavad Gita. The assistant supports multilingual voice interaction and ensures responses are strictly based on indexed scripture content.

---

## Application Preview

<p align="center">
  <img src="assets/app-preview.png" alt="Bhagavad Gita RAG Assistant UI" width="900"/>
</p>

---

## Overview

The Bhagavad Gita RAG Assistant is designed to:

- Answer philosophical and practical life questions using authentic verses
- Provide precise chapter and verse citations
- Support multilingual voice input and output
- Offer emotion-based guidance grounded in scripture
- Deliver a daily verse for reflection

The system prevents hallucinated responses by restricting generation to retrieved Gita content.

---

## Architecture

The application follows a structured RAG pipeline:

1. User Query (Text or Voice)
2. Speech-to-Text using Whisper
3. Embedding Generation
4. Vector Search in Qdrant
5. Context Retrieval (Relevant Verses)
6. LLM Response Generation using LLaMA 3.1 (Groq API)
7. Text-to-Speech Output using gTTS

This architecture ensures that every answer is traceable to scripture.

---

## Core Features

### 1. Scripture-Based Question Answering

- Retrieves semantically relevant verses
- Generates contextual explanations
- Always includes chapter and verse references

Example:

> "What does the Gita say about anger?"  
Returns verses such as Chapter 2, Verse 62–63.

---

### 2. Voice Interaction

- Users can speak queries directly
- Whisper converts speech to text
- Responses are converted back to speech using gTTS
- Supports multilingual voice queries

---

### 3. Multilingual Support

Supported languages:

- English
- Hindi
- Kannada
- Sanskrit

The assistant detects language context and generates responses accordingly.

---

### 4. Emotion-Based Guidance

Users can express emotional states such as:

- "I am confused"
- "I feel angry"
- "I feel hopeless"

The system maps emotional intent to relevant verses and provides contextual interpretation.

---

### 5. Verse of the Day

Provides:

- Sanskrit Shloka
- Transliteration
- Translation
- Brief explanation

---

## Tech Stack

### Frontend
- Streamlit

### LLM
- LLaMA 3.1 via Groq API

### Vector Database
- Qdrant

### Orchestration
- LangGraph

### Voice Stack
- Whisper (Speech-to-Text)
- gTTS (Text-to-Speech)

### Embeddings
- Compatible embedding model (e.g., OpenAI or Groq-supported model)

---

## Project Structure
