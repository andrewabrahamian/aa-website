import json
from pathlib import Path

from app.services.nutrients import extract_nutrients_per_100g, per_gram_from_per_100g, compute_for_grams


def test_extract_nutrients_from_fixture():
    fixture = json.loads((Path(__file__).resolve().parent.parent / "fixtures" / "fdc_food_sample.json").read_text())
    nutrients = extract_nutrients_per_100g(fixture)
    assert nutrients["kcal"] == 148
    assert nutrients["protein_g"] == 10.0
    assert nutrients["sodium_mg"] == 140


def test_compute_for_grams_math():
    per_gram = per_gram_from_per_100g({"kcal": 200, "protein_g": 10})
    result = compute_for_grams(per_gram, 150)
    assert result["kcal"] == 300
    assert result["protein_g"] == 15
