import numpy as np
from scipy.signal import argrelextrema
import yfinance as yf
import pandas as pd
from collections import defaultdict
from ta import trend


def get_livequote(sym, period,interval):
    tickers = yf.Ticker(sym)
    dataframe_=tickers.history(period=period, interval=interval,actions=False)
    dataframe_=dataframe_.reset_index()

    ##rename the columns    
    df = dataframe_.rename(columns={ 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume','Datetime':'timestamp'})

    df['tikr']=sym
 
    df.sort_index(inplace=True)
    ##extract the columns you want
    df = df[['tikr','open', 'high', 'low', 'close', 'volume','timestamp']]
    return df

def get_max_min2(prices):
    priceshigh['high'] = trend.ema_indicator(prices["high"], fillna=True)
    priceslow['low'] = trend.ema_indicator(prices["low"], fillna=True)
    new_high=pd.DataFrame()
    new_low=pd.DataFrame()
    for i in prices.index:
        if i == 0 or i >=prices.shape[0]-1:
            pass
        elif prices['high'][i-1] < prices['high'][i] > prices['high'][i+1]:
            new_high=new_high.append(prices.iloc[[i]])
        elif prices['low'][i-1] > prices['low'][i] <prices['low'][i+1]:
            new_low=new_low.append(prices.iloc[[i]])
        else:
            pass
    return new_high,new_low
        





    
    


# def get_max_min(prices, smoothing, window_range):
#     smooth_prices = prices['close'].rolling(window=smoothing).mean().dropna()
#     local_max = argrelextrema(smooth_prices.values, np.greater)[0]
#     local_min = argrelextrema(smooth_prices.values, np.less)[0]
#     price_local_max_dt = []
#     for i in local_max:
#         if (i>window_range) and (i<len(prices)-window_range):
#             price_local_max_dt.append(prices.iloc[i-window_range:i+window_range]['close'].idxmax())
#     price_local_min_dt = []
#     for i in local_min:
#         if (i>window_range) and (i<len(prices)-window_range):
#             price_local_min_dt.append(prices.iloc[i-window_range:i+window_range]['close'].idxmin())  
#     maxima = pd.DataFrame(prices.loc[price_local_max_dt])
#     minima = pd.DataFrame(prices.loc[price_local_min_dt])
#     max_min = pd.concat([maxima, minima]).sort_index()
#     max_min.index.name = 'date'
#     max_min = max_min.reset_index()
#     max_min = max_min[~max_min.date.duplicated()]
   
#     p = prices.reset_index()   
    
#     max_min['day_num'] = p[p['index'].isin(max_min.date)].index.values
#     print(max_min)
#     max_min = max_min.set_index('day_num')
   
#     return max_min





# def inverseHS(dataset):
#     patterns = defaultdict(list)
#     datapoints=dataset['close']
    
#     # Window range is 5 units
#     for i in range(5, len(datapoints)):  
#         window = datapoints.iloc[i-5:i]
        
#         # Pattern must play out in less than n units
#         if window.index[-1] - window.index[0] > 30:      
#             continue 
      
            
#         a, b, c, d, e = window.iloc[0:5]
                
#         # IHS
#         if a<b and c<a and c<e and c<d and c<b and e<d and abs(b-d)<=np.mean([b,d])*0.04:
#                patterns['IHS'].append((dataset['timestamp'][window.index[0]],dataset['timestamp'][window.index[-1]]))
        
#     return patterns

# def standardHS(dataset):
#     patterns = defaultdict(list)
#     datapoints=dataset['close']
    
#     # Window range is 5 units
#     for i in range(5, len(datapoints)):  
#         window = datapoints.iloc[i-5:i]
      

        
#         # Pattern must play out in less than n units
#         if window.index[-1] - window.index[0] > 30:      
#             continue 
      
            
#         a, b, c, d, e = window.iloc[0:5]
                
#         # IHS
#         if a>b and c>a and c>e and c>d and c>b and e>d and abs(b-d)<=np.mean([b,d])*0.01:
#                patterns['IHS'].append((dataset['timestamp'][window.index[0]],dataset['timestamp'][window.index[1]],dataset['timestamp'][window.index[2]],dataset['timestamp'][window.index[3]],dataset['timestamp'][window.index[4]]))
        
#     return patterns


def main():
    data=get_livequote('HDFC.NS','1d','1m')
    datapoints=get_max_min2(data,10)
    print (datapoints)
   
    hsPattern=standardHS(datapoints)
    print (hsPattern)
 

main()

