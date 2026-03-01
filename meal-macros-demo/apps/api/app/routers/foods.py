from fastapi import APIRouter
from app.services.fdc import fdc_search

router = APIRouter(prefix="/api/foods")


@router.get('/search')
def foods_search(q: str):
    return {"results": fdc_search(q, page_size=10)}
