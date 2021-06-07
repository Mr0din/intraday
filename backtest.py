from pymongo import MongoClient
import pandas as pd
from tikrdata import get_livequote
from scalping import adx_strategy,adx_trend,angle_trend,fibbonacciTrend,stochTrend,dayTrend,get_variance
from emastrategy import emaTrend,ema_strategy
from tikrdata import ConnectProd
from tqdm import tqdm
import sys, os


def fibretractment(data):
    diff = data['edgeHigh'][1] - data['edgeLow'][1]

    #uptrend
    uptrend=[high + 0.236 * diff,high + 0.382 * diff,high + 0.618 * diff,high - 0.236 * diff,high - 0.382 * diff,high - 0.618 * diff]
    # downtrend
    downtrend=[low - 0.236 * diff,low - 0.382 * diff,low - 0.618 * diff,low + 0.236 * diff,low + 0.382 * diff,low + 0.618 * diff ]


    return True
   


def get_max_min2(prices):
    # prices['sma'] = trend.ema_indicator(prices["close"], window=smoothing, fillna=True)
    for i in prices.index:
        if 0>i <=9 :
            prices.at[i,'edgeHigh']=max(list( prices['high'].iloc[:i]))
            prices.at[i,'edgeLow']=max(list( prices['low'].iloc[:i]))

        elif i >9:
      
            prices.at[i,'edgeHigh']=max(list( prices['high'].iloc[i-10:i]))
            prices.at[i,'edgeLow']=min(list( prices['low'].iloc[i-10:i]))
        else:
            prices.at[i,'edgeHigh']=0
            prices.at[i,'edgeLow']=0

       
    return prices
        


def backtestStrategy_live(strategyname,tikrname,strategytimeline):
    data=get_livequote(tikrname, strategytimeline,'1m') 
  
    data=data.reset_index()
    data=emaTrend(data)
    data=get_max_min2(data)
    data['new_date'] = [str(d.date()) for d in data['Datetime']]
    data['new_time'] = [d.time() for d in data['Datetime']]
    # data=data.loc[data['new_date'] == '2021-05-03']
    # data=data.reset_index(drop=True)
  
    # data=macd_trend(data)
    # data=adx_trend(data)
    # data=fibbonacciTrend(data)
    # data=stochTrend(data)
    # data=dayTrend(data)
    # data=get_variance(data)
    
    open_position=0
    start_price=0
    risk=0
    reward=0
    current_runn='waiting'
    pnl=0
    
    

    for i in tqdm(data.index):
        if i <=1 :
            pass
        else:
        

            try:
        
                strategy_data= data.iloc[i-2:i]
                trigger_start,open_position,current_runn,start_price,end_price,pnl,risk,reward=ema_strategy(strategy_data,open_position,start_price,risk,reward)
                data.at[i,'current_runn']=current_runn
                data.at[i,'trigger_start']=trigger_start
                data.at[i,'open_position']=open_position
                data.at[i,'start_price']=start_price
                data.at[i,'end_price']=end_price
                data.at[i,'pnl']=pnl
                data.at[i,'risk']=risk
                data.at[i,'reward']=reward
                # data.at[i+1,'angelBreakout']=round(angle,2)
                # data.at[i,'macd_trend']=macd_trend1
                
            except Exception as e: 
                raise e
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                            

    return data


data=backtestStrategy_live('adx_strategy','HDFCBANK.NS','7d')
data=data.fillna(0)
result_data= pd.DataFrame()
result_data['date']=list(set(list(data['new_date'])))
result_data['revenue']= [sum(list(data[data["new_date"] ==d]['pnl'])) for d in result_data['date']]

print(result_data)

data.to_csv('adx_backtest_airtel.csv')





        



