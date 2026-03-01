from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import create_db_and_tables
from app.routers.foods import router as foods_router
from app.routers.meals import router as meals_router
from app.services.storage import IMAGE_DIR

app = FastAPI(title="Meal Macros Demo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    create_db_and_tables()


app.mount("/images", StaticFiles(directory=str(IMAGE_DIR)), name="images")
app.include_router(meals_router)
app.include_router(foods_router)


@app.get('/health')
def health():
    return {"ok": True}
