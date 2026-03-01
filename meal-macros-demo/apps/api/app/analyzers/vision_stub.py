from pathlib import Path


class VisionStubAnalyzer:
    """Deterministic placeholder analyzer. Replace with real model by keeping same interface."""

    keyword_map = {
        "eggs": ["scrambled eggs", "toast", "avocado"],
        "salad": ["salad", "chicken breast", "sauce"],
        "pasta": ["pasta", "mixed vegetables", "salmon"],
        "steak": ["steak", "mixed vegetables", "rice"],
        "rice": ["rice", "chicken breast", "sauce"],
    }

    def analyze(self, filename: str):
        stem = Path(filename).stem.lower()
        for key, labels in self.keyword_map.items():
            if key in stem:
                return [{"label": l, "confidence": 0.82} for l in labels]
        return [
            {"label": "mixed meal item 1", "confidence": 0.35},
            {"label": "mixed meal item 2", "confidence": 0.35},
        ]
