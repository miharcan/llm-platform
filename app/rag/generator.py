def generate_answer(query: str, documents: list[str]) -> str:
    if not documents:
        return "No relevant documents found."

    context = " ".join(documents)
    return f"Based on retrieved documents: {context}"
