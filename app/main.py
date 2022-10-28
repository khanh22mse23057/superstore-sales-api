from fastapi import Depends, FastAPI, Header, HTTPException #import class FastAPI() từ thư viện fastapi
from .api.routers import sales


app = FastAPI(
    title="MSE Python For Enginner Assignments",
    description="Super Store Sales APIs",
    version="1.0",
)

app.include_router(sales.router, prefix="/sales")

@app.get("/info") 
async def info():
    return {"Message":'Hi ! I\'am Pham Nguyen Phu Khanh'}

