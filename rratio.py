from pymongo import MongoClient
import pandas as pd

from scalping import adx_strategy,adx_trend,angle_trend,fibbonacciTrend,stochTrend,dayTrend
from tikrdata import ConnectProd
from tqdm import tqdm
import sys, os
import statistics 
import numpy as np
import yfinance as yf
from datetime import datetime



# def get_data(tikr):
#     tiker = yf.Ticker(tikr)
#     data = tiker.history(period = "1d", interval = "1m")
#     return data

def get_variance(data):
    data=data.reset_index(drop=True)
    for i in data.index:
        if i <10:
            pass
        else:
            new_data= data[i-9:i]
           
            closepoint= new_data['Open'][i-1]
            standardDeviationHigh=statistics.stdev(new_data['High'], xbar = closepoint)
            standardDeviationLow=statistics.stdev(new_data['Low'], xbar = closepoint)
            print(standardDeviationHigh,standardDeviationLow)
    
    
    return standardDeviationHigh, StandardDeviationLow
