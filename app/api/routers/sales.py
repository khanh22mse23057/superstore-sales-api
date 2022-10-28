from fastapi import APIRouter, Request, Response, Body, HTTPException,Header,Query
from fastapi.responses import PlainTextResponse
from typing import Optional

router = APIRouter()


@router.get("/top-by-product", status_code=200)
async def read_items(index: Optional[int] = Query(5, max=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if index:
        results.update({"q": index})
    return results

@router.get("/top-by-category", status_code=200)
async def read_items(category: Optional[str] = Query(5, max_length=100)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if category:
        results.update({"q": category})
    return results