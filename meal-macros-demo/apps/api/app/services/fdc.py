import os
from typing import List
import httpx

FDC_BASE = "https://api.nal.usda.gov/fdc/v1"


def _api_key() -> str:
    return os.getenv("FDC_API_KEY", "")


def rerank_candidates(query: str, foods: List[dict]) -> List[dict]:
    tokens = [t for t in query.lower().split() if t]

    def score(item: dict) -> tuple:
        desc = (item.get("description") or "").lower()
        data_type = item.get("dataType") or ""
        type_score = 2 if data_type == "Foundation" else 1 if data_type == "SR Legacy" else 0
        token_score = sum(1 for t in tokens if t in desc)
        return (type_score, token_score)

    return sorted(foods, key=score, reverse=True)


def fdc_search(query: str, page_size: int = 10) -> List[dict]:
    key = _api_key()
    if not key:
        return []
    with httpx.Client(timeout=15) as client:
        r = client.post(
            f"{FDC_BASE}/foods/search",
            params={"api_key": key},
            json={"query": query, "pageSize": page_size},
        )
        r.raise_for_status()
        foods = r.json().get("foods", [])
    ranked = rerank_candidates(query, foods)
    return [
        {"fdc_id": f.get("fdcId"), "description": f.get("description"), "dataType": f.get("dataType")}
        for f in ranked[:page_size]
        if f.get("fdcId")
    ]


def fdc_get_food(fdc_id: int) -> dict:
    key = _api_key()
    if not key:
        return {}
    with httpx.Client(timeout=15) as client:
        r = client.get(f"{FDC_BASE}/food/{fdc_id}", params={"api_key": key})
        r.raise_for_status()
        return r.json()
