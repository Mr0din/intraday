import pandas as pd
from tikrdata import get_livequote
from ta import trend, momentum
import math
import numpy as np
import statistics
# here we are tying to get the current direction of the market 

def bottomline(buyprice,sellprice):
    no_of_shares=round(1000000/buyprice)
    turnaround=no_of_shares*(buyprice+sellprice)
    brokerage= 0.0003*turnaround
    stt= round((sellprice*no_of_shares)*0.00025)
    tc=round(turnaround*0.0000325,2)
    gst=round(0.18*(brokerage+tc),2)
    sebi=round(0.000001*turnaround,2)
    stamp=round(0.000002*turnaround,2)
    total=brokerage+stt+tc+gst+sebi+stamp
    bottomline=(sellprice-buyprice)*no_of_shares - total
    # print('Prift or loss:',bottomline)
    return bottomline

def fibbonacciTrend(data):
    data["3ema"]=round(trend.ema_indicator(data["close"], window=8, fillna=True),3)
    data["6ema"]=round(trend.ema_indicator(data["close"], window=13, fillna=True),3)
    data["9ema"]=round(trend.ema_indicator(data["close"], window=21, fillna=True),3)
    for i in data.index:
        if data["3ema"][i]> data["6ema"][i]>data["9ema"][i]  :
            data.at[i,'fibotrend']='up'
        elif data["3ema"][i]< data["6ema"][i]< data["9ema"][i]:
            data.at[i,'fibotrend']='down'
        else:
            data.at[i,'fibotrend']='no'
    return data


def dayTrend(data):
    data['SMA'] = trend.sma_indicator(data["close"], window=8, fillna=True)
    for i in data.index:
        if i == 0:
            pass
        elif data['SMA'][i]<data['SMA'][i-1]:
            data.at[i,'smatrend']='down'
        elif data['SMA'][i]>data['SMA'][i-1]:
            data.at[i,'smatrend']='up'
        else:
            data.at[i,'smatrend']='no'
    return data

# def macd_trend(data):
#     data["MACD"]=round(trend.macd(data["close"],n_slow=10, fillna=True),5,2)
#     data['macd_signal']=round(trend.macd_signal(data['close'], n_slow=10, n_sign=5, fillna=False),4)
#     return data


def adx_trend(data):
 
    data["ADX"]=trend.adx(data["high"], data["low"], data["close"], window=14, fillna=True)
    return data

def angle_trend(data):
    shift_data=data.shift(periods=1)
    data['angleBreakout']=round(np.rad2deg(np.arctan(data['ADX']-shift_data['ADX'])),2)
    data=data.fillna(0)
    return data
    


def deviation_calcualtion(data):
    min_number=min(data['macd_signal'])
    max_number=max(data['macd_signal'])
    return min_number,max_number


def macd_deicison(data):
    latest_data=data.reset_index(drop=True)
    diff= abs(latest_data['MACD'][1]-latest_data['macd_signal'][1])
    if latest_data['MACD'][1]<0 and latest_data['macd_signal'][1]<0 :
        sign='opp'
    elif latest_data['MACD'][1]>0 and latest_data['macd_signal'][1]>0 :
        sign='opp'
    else:
        sign='inline'
    if latest_data['MACD'][1]=='' or latest_data['macd_signal'][1]=='' or diff<=0.06:
        trend_='no' 
    elif latest_data['MACD'][1]>latest_data['macd_signal'][1]:
        trend_='up'
    elif latest_data['MACD'][1]<latest_data['macd_signal'][1]:
        trend_='down'
    else:
        trend_='no'
    return trend_

def get_openposition(open_position,start_price,risk,reward,data):
    low_price=data['low'][1]
    high_price=data['high'][1]
    postion_type=data['trigger_start'][1]
    
    if postion_type==1:
        if data['ADX'][1]<data['ADX'][0]:
            open_position=0
            end_price=data['close'][1]
            current_runn='stopped'
            trigger_start=3
            pnl= round(bottomline(start_price,end_price),2)
        
        elif data['high'][1]-start_price>= reward:
            open_position=0
            end_price=start_price+reward
            current_runn='stopped'
            trigger_start=3
            pnl= round(bottomline(start_price,end_price),2)
            
        else:
            open_position=3
            end_price=0
            current_runn='waiting'
            trigger_start=data['trigger_start'][1]
            pnl= 0.00
      

    elif postion_type==0:
        if data['ADX'][1]<data['ADX'][0]:
            open_position=0
            end_price=data['close'][1]
            current_runn='stopped'
            trigger_start=3
            pnl= round(bottomline(end_price,start_price),2)
        
         
        elif data['low'][1]-start_price>= reward:
            open_position=0
            end_price=start_price-reward
            current_runn='stopped'
            trigger_start=3
            pnl= round(bottomline(end_price,start_price),2)
            
       
        else:
            open_position=3
            end_price=0
            current_runn='waiting'
            trigger_start=data['trigger_start'][1]
            pnl= 0.00
        
    else:
        end_price=0
        open_position=3
        current_runn='waiting'
        start_price=0
        trigger_start=data['trigger_start'][1]
        pnl= 0.00
       
    return end_price,open_position,current_runn,start_price,trigger_start,pnl,risk
   


def get_variance(data):
    data=data.reset_index(drop=True)
    for i in data.index:
        if i <10:
            pass
        else:
            new_data= data[i-10:i]
           
            closepoint= new_data['open'][i-1]
            standardDeviationHigh=statistics.stdev(new_data['high'], xbar = closepoint)
            standardDeviationLow=statistics.stdev(new_data['low'], xbar = closepoint)
            data.at[i,'dH']=round(standardDeviationHigh,3)
            data.at[i,'dL']=round(standardDeviationLow,3)
        
            
    
    
    return data


def stochTrend(data):
    data["stoch"]=momentum.stoch(data["high"], data["low"], data["close"], window=8, fillna=True)
    for i in data.index:
        if data["stoch"][i]>=80:
            data.at[i,'stochtrend']='down'
        elif data["stoch"][i]<=20:
            data .at[i,'stochtrend']='up'
        elif 50>=data["stoch"][i]>=40:
            data.at[i,'stochtrend']='any'
        else:
            data.at[i,'stochtrend']='no'

    return data



        


def adx_strategy(data,open_position,start_price,risk):
    latest_data =data.reset_index(drop=True)
     
    angle_in_radians = math.atan(latest_data['ADX'][1]-latest_data['ADX'][0])
    angle_in_degrees = round(math.degrees(angle_in_radians),2)
    macd_trend= latest_data['fibotrend'][1]
    stochtrend= latest_data['stochtrend'][1]
    daytrend=latest_data['smatrend'][1]
    if open_position==0 and latest_data['ADX'][1]>=30 and angle_in_degrees>50 :
        pnl= 0.00
        
        #starting a signal
        if daytrend=='up'  :
            trigger_start=0#buy
            open_position=1
            current_runn='start'
            start_price=latest_data['close'][1]
            end_price=0
            risk= now_price =latest_data['dL'][1]
        elif daytrend=='down': 
            trigger_start=1#sell
            open_position=1
            current_runn='start'
            start_price=latest_data['close'][1]
            end_price=0
            risk= now_price =latest_data['dH'][1]
        else: 
            trigger_start=3#sell
            open_position=0
            current_runn='waiting'
            start_price=0
            end_price=0
            risk= 0

       
    elif open_position==1 or open_position==3: 
        now_price =latest_data['close'][1]

        end_price,open_position,current_runn,start_price,trigger_start,pnl,risk=get_openposition(open_position,start_price,2,6,latest_data)
        



    else:
        trigger_start=3#waiting
        open_position=0
        current_runn='waiting'
        start_price=0
        end_price=0
        pnl= 0.00
        risk=0

    return trigger_start,open_position,current_runn,angle_in_degrees,macd_trend,start_price,end_price,pnl,risk

##starting
# MGL 3.2,6,5 : HDFC
###############################ending
# def entryangle_strategy(data,open_position):
#     latest_data =data.reset_index(drop=True)
#     macd_trend= macd_deicison(data)
#     # getting sign change
#     if latest_data['angleBreakout'][0]<=0 and latest_data['angleBreakout'][1]>0:
#         sign_change='yes'
#     elif latest_data['angleBreakout'][0]>=0 and latest_data['angleBreakout'][1]<0:
#         sign_change='yes'
#     else:
#         sign_change='no'
#     # getting stoppage
#     # if open_position==0 and current_purchase==0:
#     #     open_position=0
#     # elif open_position==1 and current_purchase==0:

    
#     if sign_change=='yes' and open_position==0:
        
#         #starting a signal
#         if macd_trend=='up' and open_position==0 :
#             current_purchase=latest_data['open'][1]
#             trigger_start=1#buy
#             open_position=1
#             current_runn='start'
#         elif macd_trend=='down' and open_position==0: 
#             current_purchase=latest_data['open'][1]
#             trigger_start=0#sell
#             open_position=1
#             current_runn='start'
     
#     elif open_position==1: 
#         if latest_data['ADX'][1]<=25 : 
#             trigger_start=latest_data['trigger_start'][0]
#             open_position=0
#             current_runn='end'
#         elif latest_data['ADX'][1]>25 : 
#             trigger_start=latest_data['trigger_start'][0]
#             open_position=1
#             current_runn='continue'
#         else: 
#             trigger_start=3#waiting
#             open_position=0
#             current_runn='waiting'
#     else:
#         trigger_start=3#waiting
#         open_position=0
#         current_runn='waiting'

#     return trigger_start,open_position,current_runn,macd_trend







    

