SERVING_PRIORS = {
    "scrambled eggs": 120,
    "rice": 180,
    "chicken breast": 140,
    "salad": 150,
    "avocado": 75,
    "toast": 35,
    "pasta": 200,
    "steak": 200,
    "salmon": 170,
    "mixed vegetables": 150,
    "sauce": 30,
}


def normalize_label(label: str) -> str:
    return " ".join(label.lower().strip().split())


def estimate_grams(label: str, multiplier: float = 1.0):
    normalized = normalize_label(label)
    base = SERVING_PRIORS.get(normalized, 150)
    confidence = 0.75 if normalized in SERVING_PRIORS else 0.45
    # Placeholder hook for future area-based scaling.
    return base * multiplier, confidence
