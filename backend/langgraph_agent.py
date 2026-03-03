import json
from typing_extensions import TypedDict
from typing import List, Dict, Any
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
    intents: List[str]
    current_intent: str
    parameters: dict
    replies: List[dict]
    reply: dict
    retry_count: int
    run_retry: bool

# -------------------------
# Planner Node Phase 6 (Multi-Intent)
# -------------------------
def planner_node(state: ChatState):
    user_text = state["messages"][-1]["content"]
    retry_count = state.get("retry_count", 0)
    
    context = ""
    if retry_count > 0:
        context = "NOTE: The previous search either had low confidence (< 50%) or lacked explicit Chapter/Verse citations. Please refine your intents or use more specific keywords in parameters."

    planning_prompt = f"""
You are an AI intent planner for a Bhagavad Gita assistant.
{context}

Available intents:
- question
- emotion
- life_phase
- daily_verse
- random_verse
- greeting (for simple hellos, hi, what's your name, how are you)

User message:
"{user_text}"

You can select MULTIPLE intents if the user's message is complex (e.g., mixing an emotion with a question).
Return ONLY valid JSON:
{{
  "intents": ["..."],
  "parameters": {{}}
}}
"""

    response = llm.invoke(planning_prompt)

    try:
        clean_content = response.content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:-3].strip()
        elif clean_content.startswith("```"):
            clean_content = clean_content[3:-3].strip()
            
        decision = json.loads(clean_content)
        
        if "intents" in decision:
            state["intents"] = decision["intents"]
        elif "intent" in decision:
            state["intents"] = [decision["intent"]]
        else:
            state["intents"] = ["question"]
            
        state["parameters"] = decision.get("parameters", {})
    except Exception as e:
        print(f"Planner error parsing JSON: {e}")
        state["intents"] = ["question"]
        state["parameters"] = {}

    state["replies"] = []
    # Initialize retry_count if not set
    if "retry_count" not in state:
        state["retry_count"] = 0
        
    return state

# -------------------------
# Intent Router Node Phase 6
# -------------------------
def intent_router_node(state: ChatState):
    intents = state.get("intents", [])
    if intents:
        next_intent = intents[0]
        state["intents"] = intents[1:]
        state["current_intent"] = next_intent
    else:
        state["current_intent"] = "critic"
    return state

def route_intent(state: ChatState):
    intent = state.get("current_intent", "critic")
    valid_intents = ["question", "emotion", "life_phase", "daily_verse", "random_verse", "greeting"]
    if intent in valid_intents:
        return intent
    return "critic"

# -------------------------
# Nodes Phase 4 (Using Parameters)
# -------------------------
def question_node(state: ChatState):
    res = ask_gita(state["messages"][-1]["content"])
    state["replies"] = state.get("replies", []) + [res]
    return state

def emotion_node(state: ChatState):
    emotion = state.get("parameters", {}).get("emotion")
    if emotion:
        res = ask_gita_by_emotion(emotion.capitalize())
    else:
        res = ask_gita(state["messages"][-1]["content"])
    state["replies"] = state.get("replies", []) + [res]
    return state

def life_phase_node(state: ChatState):
    phase = state.get("parameters", {}).get("phase")
    if phase:
        res = ask_gita_by_life_phase(phase.capitalize())
    else:
        res = ask_gita(state["messages"][-1]["content"])
    state["replies"] = state.get("replies", []) + [res]
    return state

def daily_verse_node(state: ChatState):
    res = get_verse_of_the_day()
    state["replies"] = state.get("replies", []) + [res]
    return state

def random_verse_node(state: ChatState):
    res = get_random_verse()
    state["replies"] = state.get("replies", []) + [res]
    return state

def greeting_node(state: ChatState):
    user_text = state["messages"][-1]["content"]
    prompt = f"""You are GitaMind, an AI Bhagavad Gita Assistant.
The user just said: "{user_text}"

INSTRUCTIONS:
1. Respond warmly and concisely in Maximum 1 or 2 sentences.
2. If they shared their name, use it (e.g., "Namaste Abhinav...").
3. Tell them you are here to guide them using the wisdom of the Bhagavad Gita.
4. DO NOT generate, invent, or recite any verses. Do not hallucinate scriptures. Stop writing after your brief greeting. DO NOT repeat yourself."""
    
    response = llm.invoke([{"role": "system", "content": prompt}])
    
    res = {
        "answer": response.content.strip(),
        "confidence": 100,
        "provenance": [],
        "is_greeting": True
    }
    state["replies"] = state.get("replies", []) + [res]
    return state

# -------------------------
# Critic Node Phase 7 (Reflection Loop)
# -------------------------
def critic_node(state: ChatState):
    replies = state.get("replies", [])
    retry_count = state.get("retry_count", 0)
    
    has_grounding = any(r.get("confidence", 0) > 50 for r in replies)
    has_citation = any("chapter" in r.get("answer", "").lower() and "verse" in r.get("answer", "").lower() for r in replies)
    is_greeting = any(r.get("is_greeting", False) for r in replies)
    
    # If no valid answers found or missing citations, and we haven't maxed out retries
    if not is_greeting and (not has_grounding or not has_citation) and retry_count < 2:
        state["retry_count"] = retry_count + 1
        state["run_retry"] = True
        return state
        
    state["run_retry"] = False
    
    # Combine successful replies
    answers = []
    max_confidence = 0
    prov_seen = set()
    unique_prov = []
    
    for r in replies:
        if r.get("answer"):
            # Avoid repeating exactly the same answer block if multiple intents yield same
            if r["answer"] not in answers:
                answers.append(r["answer"])
        if r.get("confidence", 0) > max_confidence:
            max_confidence = r.get("confidence", 0)
        for p in r.get("provenance", []):
            key = (p.get("page"), p.get("source"))
            if key not in prov_seen:
                prov_seen.add(key)
                unique_prov.append(p)
                
    combined_answer = "\n\n".join(answers)
    if not combined_answer.strip():
        combined_answer = "I could not find a relevant answer in the Bhagavad Gita based on your query."
        
    state["reply"] = {
        "answer": combined_answer,
        "confidence": max_confidence,
        "provenance": unique_prov
    }
    return state

def evaluate_critic(state: ChatState):
    if state.get("run_retry"):
        return "planner"
    return END

# -------------------------
# Graph Phase 5 & 7 Rebuild
# -------------------------
graph = StateGraph(ChatState)

graph.add_node("planner", planner_node)
graph.add_node("intent_router", intent_router_node)
graph.add_node("question", question_node)
graph.add_node("emotion", emotion_node)
graph.add_node("life_phase", life_phase_node)
graph.add_node("daily_verse", daily_verse_node)
graph.add_node("random_verse", random_verse_node)
graph.add_node("greeting", greeting_node)
graph.add_node("critic", critic_node)

graph.set_entry_point("planner")

# From planner, go to router to deal out intents
graph.add_edge("planner", "intent_router")

# Router evaluates intents and loops or goes to critic
graph.add_conditional_edges(
    "intent_router",
    route_intent,
    {
        "question": "question",
        "emotion": "emotion",
        "life_phase": "life_phase",
        "daily_verse": "daily_verse",
        "random_verse": "random_verse",
        "greeting": "greeting",
        "critic": "critic"
    }
)

# After action nodes return, always go back to router to pop next intent
graph.add_edge("question", "intent_router")
graph.add_edge("emotion", "intent_router")
graph.add_edge("life_phase", "intent_router")
graph.add_edge("daily_verse", "intent_router")
graph.add_edge("random_verse", "intent_router")
graph.add_edge("greeting", "intent_router")

# Critic evaluates grounding and either ends or loops
graph.add_conditional_edges(
    "critic",
    evaluate_critic,
    {
        "planner": "planner",
        END: END
    }
)

agent = graph.compile()
