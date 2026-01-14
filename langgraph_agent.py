from typing_extensions import TypedDict
from typing import List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from rag_engine import (
    ask_gita,
    ask_gita_by_emotion,
    ask_gita_by_life_phase,
    get_verse_of_the_day,
    get_random_verse
)

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

class ChatState(TypedDict):
    messages: List[Dict]
    reply: dict

# -------------------------
# Smart Router
# -------------------------
def router(state):
    text = state["messages"][-1]["content"].lower()

    if "today" in text or "daily" in text:
        return "daily_verse"

    if any(k in text for k in ["another", "new", "random", "more", "verse", "sloka", "quote"]):
        return "random_verse"

    if any(k in text for k in ["anxious","angry","sad","confused","peace"]):
        return "emotion"

    if any(k in text for k in ["student","professional","leader","family"]):
        return "life_phase"

    return "question"

# -------------------------
# Nodes
# -------------------------
def question_node(state):
    state["reply"] = ask_gita(state["messages"][-1]["content"])
    return state

def emotion_node(state):
    text = state["messages"][-1]["content"].lower()
    for e in ["anxious","angry","confused","sad","peace"]:
        if e in text:
            state["reply"] = ask_gita_by_emotion(e.capitalize())
            return state
    state["reply"] = ask_gita(text)
    return state

def life_phase_node(state):
    text = state["messages"][-1]["content"].lower()
    for p in ["student","professional","leader","family"]:
        if p in text:
            state["reply"] = ask_gita_by_life_phase(p.capitalize())
            return state
    state["reply"] = ask_gita(text)
    return state

def daily_verse_node(state):
    state["reply"] = get_verse_of_the_day()
    return state

def random_verse_node(state):
    state["reply"] = get_random_verse()
    return state

# -------------------------
# Graph
# -------------------------
graph = StateGraph(ChatState)

graph.add_node("question", question_node)
graph.add_node("emotion", emotion_node)
graph.add_node("life_phase", life_phase_node)
graph.add_node("daily_verse", daily_verse_node)
graph.add_node("random_verse", random_verse_node)

graph.add_conditional_edges(
    START,
    router,
    {
        "question": "question",
        "emotion": "emotion",
        "life_phase": "life_phase",
        "daily_verse": "daily_verse",
        "random_verse": "random_verse"
    }
)

graph.add_edge("question", END)
graph.add_edge("emotion", END)
graph.add_edge("life_phase", END)
graph.add_edge("daily_verse", END)
graph.add_edge("random_verse", END)

agent = graph.compile()
