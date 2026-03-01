from typing import Dict, Iterable

NUTRIENT_KEYS = {
    "energy": "kcal",
    "protein": "protein_g",
    "carbohydrate, by difference": "carbs_g",
    "total lipid (fat)": "fat_g",
    "fiber, total dietary": "fiber_g",
    "sugars, total including nlea": "sugar_g",
    "sodium, na": "sodium_mg",
    "potassium, k": "potassium_mg",
    "calcium, ca": "calcium_mg",
    "iron, fe": "iron_mg",
    "vitamin c, total ascorbic acid": "vitamin_c_mg",
    "vitamin a, rae": "vitamin_a_ug_rae",
}
DEFAULT_NUTRIENTS = {v: 0.0 for v in NUTRIENT_KEYS.values()}


def extract_nutrients_per_100g(food_payload: dict) -> Dict[str, float]:
    out = DEFAULT_NUTRIENTS.copy()
    for nutrient in food_payload.get("foodNutrients", []):
        name = (nutrient.get("nutrient", {}) or {}).get("name", "").lower()
        if name in NUTRIENT_KEYS:
            out[NUTRIENT_KEYS[name]] = float(nutrient.get("amount") or 0.0)
    return out


def per_gram_from_per_100g(nutrients_100g: Dict[str, float]) -> Dict[str, float]:
    return {k: v / 100.0 for k, v in nutrients_100g.items()}


def compute_for_grams(per_gram: Dict[str, float], grams: float) -> Dict[str, float]:
    return {k: per_gram.get(k, 0.0) * grams for k in DEFAULT_NUTRIENTS}


def sum_nutrients(rows: Iterable[Dict[str, float]]) -> Dict[str, float]:
    total = DEFAULT_NUTRIENTS.copy()
    for row in rows:
        for k in total:
            total[k] += row.get(k, 0.0)
    return total
