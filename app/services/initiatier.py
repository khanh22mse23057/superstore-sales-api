from datetime import datetime
import itertools
import statsmodels.api as sm # Statsmodels là một gói Python cho phép người dùng khám phá dữ liệu : https://www.statsmodels.org/stable/index.html
# import matplotlib.pyplot as plt
# import matplotlib
import pandas as pd
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import adfuller

import warnings
warnings.filterwarnings("ignore") # Ẩn warnings khi runtime, nếu muốn xem uncomment

# train_src = []
os_y = []

def load_train_data():
    # Load data
    train_raw_url = "https://raw.githubusercontent.com/khanh22mse23057/kaggle-sales-dataset-train/main/superstore_sales.csv"

    # Đọc dữ liệu từ file csv vào data frame
    train_sales = pd.read_csv(train_raw_url)
    #train_sales.info()

    return train_sales

def pre_processing_data(df):

    data = df
    data['Postal Code'] = data['Postal Code'].astype('object') 
    data["Postal Code"] = data["Postal Code"].fillna(0)
    data["Order Date"] = pd.to_datetime(data["Order Date"], format="%d/%m/%Y")
    data["Ship Date"] = pd.to_datetime(data["Ship Date"], format="%d/%m/%Y")


    return data

def prediction_by_cat(data, cat_name):
    print("----------- Start Forecase by " + cat_name)
    cat = data.loc[data['Category']== cat_name]

    o_s = cat.loc[:, ["Order Date", "Sales"]]
    os = o_s.sort_values('Order Date')
    os = os.set_index('Order Date')
    os_y = os['Sales'].resample('MS').mean()

    decomposition_os = sm.tsa.seasonal_decompose(os_y,model='additive')
    p=d=q=range(0,2)
    pdq = list(itertools.product(p,d,q))
    seasonal_pdq = [(x[0],x[1],x[2], 12) for x in pdq]

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(os_y,order = param, seasonal_order = param_seasonal ,
                                                enforce_stationarity= False , enforce_invertibility= False )
                results = mod.fit()            
                #print('ARIMA{} x {} 12 -- AIC : {}'.format(param, param_seasonal, results.aic))            
            except:
                continue

    mod_os = sm.tsa.statespace.SARIMAX(os_y,
                                order=(1,1,1),
                                seasonal_order= (1,1,1,12),
                                enforce_stationarity = False,
                                enforce_invertibility=False)

    results_os = mod_os.fit()
    return results_os

def get_prediction_to(results_os, endDate):

  print(endDate)
  dt1 = datetime.strptime("2017/01/01", "%Y/%m/%d")
  dt2 = datetime.strptime(str(endDate), "%Y/%m/%d") 
  today = pd.to_datetime('today')
  steps = dt2 - dt1 if today > dt2 else (dt2 - today)

  return get_predictions(results_os, steps.days)

def get_predictions(results_os, steps = 100):
  pred_uc = results_os.get_forecast(steps)
  pred_ci = pred_uc.conf_int()
  df = pd.DataFrame(data=pred_ci).reset_index().rename(columns={"index": "Date", "lower Sales" : "Lower_Sale", "upper Sales" : "Upper_Sales", })  
  return df
  
def get_sale_means(results_os, startDate):
  pred_os = results_os.get_prediction(start = pd.to_datetime(startDate), dynamic = False)
  pred_ci_os = pred_os.conf_int()
  cat_forecasted = pred_os.predicted_mean

  cat_truth = os_y[startDate:]
#   print(office_truth)
  mse = ((cat_forecasted - cat_truth) ** 2).mean()
  return mse

