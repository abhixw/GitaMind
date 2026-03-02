from rag_engine import ask_gita

print("🕉️ Bhagavad Gita Assistant (type 'exit' to quit)\n")

while True:
    user_query = input("❓ Ask: ")
    if user_query.lower() == "exit":
        break

    result = ask_gita(user_query)

    print("\nAnswer:\n")
    print(result["answer"])

    if result["source"]:
        print("\nSource:\n")
        print(result["source"])
