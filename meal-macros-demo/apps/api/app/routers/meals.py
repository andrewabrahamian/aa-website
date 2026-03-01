from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, select

from app.analyzers.vision_stub import VisionStubAnalyzer
from app.database import get_session
from app.models import Meal, MealItem
from app.schemas import ConfirmRequest
from app.services.fdc import fdc_get_food, fdc_search
from app.services.nutrients import (
    compute_for_grams,
    extract_nutrients_per_100g,
    per_gram_from_per_100g,
    sum_nutrients,
)
from app.services.portion import estimate_grams
from app.services.storage import hash_bytes, save_image

router = APIRouter(prefix="/api")
analyzer = VisionStubAnalyzer()


@router.post("/meals/analyze")
async def analyze_meal(image: UploadFile = File(...), session: Session = Depends(get_session)):
    content = await image.read()
    image_hash = hash_bytes(content)

    existing = session.exec(select(Meal).where(Meal.image_hash == image_hash)).first()
    if existing:
        items = session.exec(select(MealItem).where(MealItem.meal_id == existing.id)).all()
        return format_meal_response(existing, items)

    image_path = save_image(image, content, image_hash)
    guesses = analyzer.analyze(image.filename or "upload.jpg")

    meal = Meal(image_path=image_path, image_hash=image_hash, totals_estimated_json={})
    session.add(meal)
    session.commit()
    session.refresh(meal)

    rows = []
    for guess in guesses:
        label = guess["label"]
        grams, portion_conf = estimate_grams(label)
        candidates = fdc_search(label, page_size=5)
        chosen = candidates[0] if candidates else None
        food_payload = fdc_get_food(chosen["fdc_id"]) if chosen else {}
        nutrients_100 = extract_nutrients_per_100g(food_payload)
        per_gram = per_gram_from_per_100g(nutrients_100)
        nutrients = compute_for_grams(per_gram, grams)
        item = MealItem(
            meal_id=meal.id,
            name_guess=label,
            fdc_id=chosen["fdc_id"] if chosen else None,
            fdc_description=chosen["description"] if chosen else None,
            grams_estimated=grams,
            confidence_recognition=guess["confidence"],
            confidence_match=0.7 if chosen else 0.2,
            confidence_portion=portion_conf,
            nutrients_estimated_json=nutrients,
            fdc_candidates_json={"candidates": candidates},
            per_gram_nutrients_json=per_gram,
        )
        session.add(item)
        rows.append(item)

    session.commit()
    totals = sum_nutrients([r.nutrients_estimated_json for r in rows])
    meal.totals_estimated_json = totals
    session.add(meal)
    session.commit()
    for r in rows:
        session.refresh(r)
    session.refresh(meal)
    return format_meal_response(meal, rows)


@router.post("/meals/confirm")
def confirm_meal(payload: ConfirmRequest, session: Session = Depends(get_session)):
    meal = session.get(Meal, payload.meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    final_nutrients = []
    for edit in payload.items:
        item = session.get(MealItem, edit.item_id)
        if not item or item.meal_id != meal.id:
            continue
        food_payload = fdc_get_food(edit.fdc_id)
        nutrients_100 = extract_nutrients_per_100g(food_payload)
        per_gram = per_gram_from_per_100g(nutrients_100)
        nutrients = compute_for_grams(per_gram, edit.grams_final)

        item.fdc_id = edit.fdc_id
        item.grams_final = edit.grams_final
        item.nutrients_final_json = nutrients
        item.fdc_description = food_payload.get("description", item.fdc_description)
        item.per_gram_nutrients_json = per_gram
        final_nutrients.append(nutrients)
        session.add(item)

    meal.status = "confirmed"
    meal.totals_final_json = sum_nutrients(final_nutrients)
    session.add(meal)
    session.commit()

    items = session.exec(select(MealItem).where(MealItem.meal_id == meal.id)).all()
    return format_meal_response(meal, items)


@router.get("/meals/{meal_id}")
def get_meal(meal_id: str, session: Session = Depends(get_session)):
    meal = session.get(Meal, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    items = session.exec(select(MealItem).where(MealItem.meal_id == meal.id)).all()
    return format_meal_response(meal, items)


def format_meal_response(meal: Meal, items: list[MealItem]):
    item_rows = []
    for item in items:
        nutrients = item.nutrients_final_json if meal.status == "confirmed" and item.nutrients_final_json else item.nutrients_estimated_json
        item_rows.append(
            {
                "id": item.id,
                "name_guess": item.name_guess,
                "fdc_match": {
                    "fdc_id": item.fdc_id,
                    "description": item.fdc_description,
                    "dataType": None,
                    "candidates": item.fdc_candidates_json.get("candidates", []),
                },
                "grams_estimated": item.grams_final or item.grams_estimated,
                "portion_multiplier": item.portion_multiplier,
                "confidence": {
                    "recognition": item.confidence_recognition,
                    "match": item.confidence_match,
                    "portion": item.confidence_portion,
                },
                "nutrients": nutrients,
                "per_gram_nutrients": item.per_gram_nutrients_json,
            }
        )

    totals = meal.totals_final_json if meal.status == "confirmed" and meal.totals_final_json else meal.totals_estimated_json
    return {
        "meal": {
            "id": meal.id,
            "created_at": meal.created_at,
            "image_path": f"/images/{meal.image_path.split('/')[-1]}",
            "image_hash": meal.image_hash,
            "status": meal.status,
        },
        "items": item_rows,
        "totals": totals,
        "disclaimer": "Estimates only. Portion sizes may be inaccurate.",
    }
