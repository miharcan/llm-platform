def estimate_token_cost(text: str) -> float:
    tokens = len(text.split())
    return tokens * 0.00001
