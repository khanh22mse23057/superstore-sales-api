from datetime import date
from fastapi import APIRouter, Request, Response, Body, HTTPException,Header,Query
from fastapi.responses import PlainTextResponse
from typing import Optional

from setuptools import Require
from app.services import initiatier
import json
import pandas as pd
from app import main
from pandas import json_normalize 
from pydantic import BaseModel
import numpy

router = APIRouter()

@router.get("/top-by-product", status_code=200)
async def get_top_product(top: Optional[int] = Query(5, max=50)):
    top_product_sales = main.data.groupby(["Product ID", "Product Name"])["Sales"].sum().reset_index(name="Sales").sort_values("Sales", ascending= False)

    r = pd.DataFrame.from_dict(top_product_sales[:top].to_dict(), orient='index').to_dict()
    result = []
    for k in r:
        result.append(r[k])
    return result

@router.get("/top-by-city", status_code=200)
async def get_top_city(top: Optional[int] = Query(5, max=50)):
    top_city_sales = main.data.groupby(["City"])["Sales"].sum().reset_index(name="Sales").sort_values("Sales", ascending= False)
    r = pd.DataFrame.from_dict(top_city_sales[:top].to_dict(), orient='index').to_dict()
    result = []
    for k in r:
        result.append(r[k])
    return result

@router.get("/get-category", status_code=200)
async def get_category():
    src = main.data
    results = src['Category'].unique()

    return list(results)

class ForecastSale(BaseModel):
    Date: str
    Lower_Sale: float
    Upper_Sales: float

@router.get("/forecast-by-category", status_code=200)
async def forecast_sale_by_category(category: str, toDate : date):

    d_cat = ['Furniture', 'Office Supplies', 'Technology']
    try:
        if category not in d_cat:
            return {"Error":'Category not found', "Category List" :d_cat }

        endDate = pd.to_datetime(toDate, format='%Y/%m/%d')
        print(category)
        print(toDate)
        #r_train = main.Cat_Train_Result[category]  else initiatier.prediction_by_cat(main.data, category)

        if category not in main.Cat_Train_Result:
            main.Cat_Train_Result[category] = initiatier.prediction_by_cat(main.data, category)
           
        r_train = main.Cat_Train_Result[category]
        print(r_train)
        result =  initiatier.get_prediction_to(r_train, endDate.strftime('%Y/%m/%d'))
        # pre_r = result[result['Date'] < endDate]
        pre_r = result[(result['Date'] >= pd.to_datetime('today')) &  (result['Date'] <= endDate)]

        r = pd.DataFrame.from_dict(pre_r.to_dict(), orient='index').to_dict()
        result = []
        for k in r:
            result.append(r[k])
        return result

    except Exception as e: print(e)
    
    return {"Error":'Cannt forecast sales'}


