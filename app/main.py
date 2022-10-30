from unittest import result
from fastapi import Depends, FastAPI, Header, HTTPException #import class FastAPI() từ thư viện fastapi
from .api.routers import sales
from .services import initiatier

import datetime
import itertools 
# import matplotlib
import numpy as np
import pandas as pd

app = FastAPI(
    title="MSE Python For Enginner Assignments",
    description="Super Store Sales APIs",
    version="1.0",
)

train_sales_raw = initiatier.load_train_data()
data = initiatier.pre_processing_data(train_sales_raw.copy())

Cat_Train_Result = {}
# Furniture_Train = initiatier.prediction_by_cat(data, 'Furniture')
# Office_Supplies_Train = initiatier.prediction_by_cat(data, 'Office Supplies')
# Technology_Train = initiatier.prediction_by_cat(data, 'Technology')

app.include_router(sales.router, prefix="/sales")

@app.get("/") 
async def root():
    return {"Message":'Hi ! I\'am Pham Nguyen Phu Khanh'}

