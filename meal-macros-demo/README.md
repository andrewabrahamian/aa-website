# Meal Macros Demo

Demo web app to upload a meal photo and estimate meal components + macro/micronutrients with minimal corrections.

## Stack
- **Web:** Next.js App Router + TypeScript + Tailwind
- **API:** FastAPI + Uvicorn
- **DB:** SQLite (SQLModel)
- **Nutrition source:** USDA FoodData Central API

## Repo layout
```
meal-macros-demo/
  apps/
    web/
    api/
  packages/
    shared/
  infra/
    docker-compose.yml
```

## Setup
1. Create env files:
   - `cp apps/api/.env.example apps/api/.env`
   - `cp apps/web/.env.example apps/web/.env`
2. Add your USDA key to `apps/api/.env` as `FDC_API_KEY`.
3. Start services:
   - `cd infra && docker compose up`
4. Open web at `http://localhost:3000`.

## API endpoints
- `POST /api/meals/analyze` (multipart `image`)
- `POST /api/meals/confirm`
- `GET /api/foods/search?q=...`
- `GET /api/meals/{meal_id}`

## MVP notes / limitations
- Vision is currently a deterministic filename-keyword stub (`analyzers/vision_stub.py`).
- Portion estimation uses static serving priors; unknown items fallback to 150g with lower confidence.
- Same uploaded image bytes return cached draft results by `image_hash`.
- If FDC key is missing or search fails, item nutrients will be near-zero and still render for demo continuity.

## Nutrients included
- kcal, protein, carbs, fat, fiber, sugar
- sodium, potassium, calcium, iron
- vitamin C, vitamin A (RAE)

## Screenshot
Add screenshot here after running locally:

`![demo screenshot](./docs/screenshot-placeholder.png)`
