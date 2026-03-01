from app.services.portion import estimate_grams


def test_serving_prior_found():
    grams, confidence = estimate_grams("rice")
    assert grams == 180
    assert confidence > 0.7


def test_serving_prior_fallback():
    grams, confidence = estimate_grams("unknown food blob")
    assert grams == 150
    assert confidence < 0.5
