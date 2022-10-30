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

router = APIRouter()

@router.get("/top-by-product", status_code=200)
async def get_top_product(index: Optional[int] = Query(5, max=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if index:
        results.update({"q": index})
    return results

@router.get("/top-by-category", status_code=200)
async def get_top_category(category: Optional[str] = Query(5, max_length=100)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if category:
        results.update({"q": category})
    return results

@router.get("/get-category", status_code=200)
async def get_category():
    src = main.data
    results = src['Category'].unique()

    return list(results)

class ForecastSale(BaseModel):
    Date: str
    Lower_Sale: float
    Upper_Sales: float

@router.get("/forecast-by-category", status_code=200, response_model=ForecastSale)
async def get_top_category(category: str, toDate : date):

    d_cat = ['Furniture', 'Office Supplies', 'Technology']
    try:
        if category not in d_cat:
            return {"Error":'Category not found', "Category List" :d_cat }

        endDate = pd.to_datetime(toDate, format='%Y/%m/%d')
        print(category)
        print(toDate)
        r_train = main.Cat_Train_Result[category] if category in main.Cat_Train_Result else initiatier.prediction_by_cat(main.data, category)
        main.Cat_Train_Result[category ] = r_train

        print(r_train)
        result =  initiatier.get_prediction_to(r_train, endDate.strftime('%Y/%m/%d'))
        # pre_r = result[result['Date'] < endDate]
        pre_r = result[(result['Date'] >= pd.to_datetime('today')) &  (result['Date'] <= endDate)]
        # pre_r['Date'] = pd.to_datetime(pre_r['Date'], format='%Y-%m-%d').strftime('%Y/%m/%d')
        print(pre_r)

        res = [(ForecastSale(row['Date'],row['Lower_Sale'],row['Upper_Sales'])) for index, row in pre_r.iterrows()]  
        return res
        # return list(map(lambda x:ForecastSale(Date=x[0],Lower_Sale=x[1], Upper_Sales = x[2]),pre_r.values.tolist()))
    except Exception as e: print(e)
    
    return {"Error":'Cannt forecast sales'}


