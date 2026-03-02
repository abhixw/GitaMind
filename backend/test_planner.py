import sys
import os

sys.path.append("/Users/abhinav/Desktop/Bhagavad-gita/Bhagavad_Gita_RAG_Assistant")

try:
    from langgraph_agent import agent
except ImportError as e:
    print(f"Failed to import agent: {e}")
    sys.exit(1)

test_queries = [
    "Give me today's verse",
    "I feel anxious",
    "I am a student",
    "What is karma yoga?",
    "I feel anxious about my duties at work"
]

for query in test_queries:
    print(f"\n--- Testing Query: '{query}' ---")
    state = {
        "messages": [{"role": "user", "content": query}]
    }
    
    # We can invoke just the planner_node to see its decision
    from langgraph_agent import planner_node
    
    try:
        new_state = planner_node(state)
        print(f"Intent: {new_state.get('intent')}")
        print(f"Parameters: {new_state.get('parameters')}")
    except Exception as e:
        print(f"Error running planner: {e}")
