import pandas as pd
from tikrdata import get_livequote
from ta import trend, momentum
import math
import numpy as np
import statistics
import math
from gannsquare import gannsquare
# here we are tying to get the current direction of the market 



def fibretractment(data):
    diff = data['edgeHigh'][1] - data['edgeLow'][1]
    #uptrend
    uptrend=[high + 0.236 * diff,high + 0.382 * diff,high + 0.618 * diff,high,high - 0.236 * diff,high - 0.382 * diff,high - 0.618 * diff]
    # downtrend
    downtrend=[low - 0.236 * diff,low - 0.382 * diff,low - 0.618 * diff,low,low + 0.236 * diff,low + 0.382 * diff,low + 0.618 * diff ]
    return uptrend,downtrend



def bottomline(buyprice,sellprice):
    no_of_shares=round(50000/buyprice)
    turnaround=no_of_shares*(buyprice+sellprice)
    brokerage= 40
    #brokerage= 40
    stt= round((sellprice*no_of_shares)*0.00025)
    tc=round(turnaround*0.0000325,2)
    gst=round(0.18*(brokerage+tc),2)
    sebi=round(0.000001*turnaround,2)
    stamp=round(0.000002*turnaround,2)
    total=brokerage+stt+tc+gst+sebi+stamp
    bottomline=((sellprice-buyprice)*no_of_shares) - total
    # print('Prift or loss:',bottomline)
    return bottomline


def slope(data_list):
    trend_list=[]
    for i in range(len(data_list)):
        if i <=2:
            trend_list.append(0)
        else:
            if data_list[i]>data_list[i-1]>data_list[i-2]>data_list[i-3]:
                trend_list.append(1)# up
            elif data_list[i]<data_list[i-1]<data_list[i-2]<data_list[i-3]:
                trend_list.append(2) # down
            else:
                trend_list.append(0)
    return trend_list
            

        
def crossover(data):
    data['crossoverPoint']=round(data["6ema"]-data["9ema"],3)
    data['crossover']=0
    for i in data.index:
        if i==0:
            data.at[i,'crossover']=0
        elif data['crossoverPoint'][i-1]<0 and data['crossoverPoint'][i]>0:
            data.at[i,'crossover']=1
        elif data['crossoverPoint'][i-1]>0 and data['crossoverPoint'][i]<0:
            data.at[i,'crossover']=1
        else:
            data.at[i,'crossover']==0
    
    return data

def adx_trend(data):
 
    data["ADX"]=trend.adx(data["high"], data["low"], data["close"], window=14, fillna=True)
    return data

def emaTrend(data):
    data["emalow"]=round(trend.sma_indicator(data["low"], window=100, fillna=True),2)
    data["emahigh"]=round(trend.ema_indicator(data["high"], window=50, fillna=True),2)
    # data['macd']=round(trend.macd_diff(data["close"], window_slow= 26, window_fast= 12, window_sign = 9, fillna = False),1)
    # # data["6ema"]=round(trend.ema_indicator(data["close"], window=50, fillna=True),2)
    # # data["9ema"]=round(trend.ema_indicator(data["close"], window=61, fillna=True),2)

    # data['rsi']=round(momentum.rsi(data["close"], window=7, fillna=True),3)
    # data["9ema"]=round(trend.ema_indicator(data["close"], window=75, fillna=True),3)
    # angle_in_radians = math.atan(data['3ema'].iloc[-1]-data['3ema'].iloc[-2])
    # angle_in_degrees = round(math.degrees(angle_in_radians),2)
    # data['3trend']=slope(data['3ema'])
    # data['6trend']=slope(data['6ema'])
    # data['9trend']=slope(data['9ema'])
    # data=crossover(data)
    for i in data.index:
        if i<=1:
            data.at[i,'ematrend']='no'
        elif  data['emahigh'][i-2]<data['emalow'][i-2] and data['emahigh'][i-1]==data['emalow'][i-1]  :
            data.at[i,'ematrend']='up'
        elif  data['emahigh'][i-2]>data['emalow'][i-2] and data['emahigh'][i-1]==data['emalow'][i-1]  :
            data.at[i,'ematrend']='down' 
      

        # if i<=2:
        #     data.at[i,'ematrend']='no'
        #     pass
        # else:
        #     # if  data["3ema"][i]> data["6ema"][i]> data["9ema"][i]>data['high'][i] and data['3trend'][i]==data['6trend'][i]==data['9trend'][i] and data['3trend'][i]!='same' and  sum(list(data['crossover'][i-3:i]))>0 :
        #     #     data.at[i,'ematrend']='up'
        #     # elif data["3ema"][i]< data["6ema"][i]< data["9ema"][i]<data['high'][i] and data['3trend'][i]==data['6trend'][i]==data['9trend'][i] and data['3trend'][i]!='same' and sum(list(data['crossover'][i-3:i]))>0  :
        #     #     data.at[i,'ematrend']='down'
        #     # elif data["3ema"][i]< data["6ema"][i]<data["9ema"][i]and data['3trend'][i]==data['6trend'][i]==data['9trend'][i] and data['3trend'][i]!='same' and data["9ema"][i]>data['high'][i]>=data["6ema"][i]  :
        #     #     data.at[i,'ematrend']='down'
        #     # elif data["3ema"][i]> data["6ema"][i]>data["9ema"][i] and data['3trend'][i]==data['6trend'][i]==data['9trend'][i] and data['3trend'][i]!='same' and  data["9ema"][i]<data['low'][i]<=data["6ema"][i] :
        #     #     data.at[i,'ematrend']='up'
        #     # elif sum(list(data['3trend'][i-3:i]))==3 and sum(list(data['6trend'][i-3:i]))==3 and sum(list(data['9trend'][i-3:i]))==3 and data["9ema"][i]<data['low'][i]<=data["6ema"][i] and data["9ema"][i]<data['6ema'][i]<data["3ema"][i] :
        #     #     data.at[i,'ematrend']='up'
        #     # elif sum(list(data['3trend'][i-3:i]))==6 and sum(list(data['6trend'][i-3:i]))==6 and sum(list(data['9trend'][i-3:i]))==6 and data["9ema"][i]>data['high'][i]>=data["6ema"][i] and data["9ema"][i]>data['6ema'][i]>data["3ema"][i]:
        #     #     data.at[i,'ematrend']='down' 
        #     # if data['close'].iloc[-1]>data['3ema'].iloc[-1] and data['low'].iloc[-2]<=data['6ema'].iloc[-2] and data["3ema"].iloc[-1]>2+data["6ema"].iloc[-1]>2+data["9ema"].iloc[-1]  and data['6trend'][i-3]==1 and data['9trend'][i-3]==1 :
        #     #     data.at[i,'ematrend']='up'
        #     # elif data['close'].iloc[-1]<data['9ema'].iloc[-1] and data['high'].iloc[-2]>=data['6ema'].iloc[-2] and data["3ema"].iloc[-1]<2+data["6ema"].iloc[-1]<2+data["9ema"].iloc[-1]  and data['6trend'][i-3]==2 and data['9trend'][i-3]==2:
        #     #     data.at[i,'ematrend']='down'

        else:
            data.at[i,'ematrend']='no'
            
    return data


def gannposition(data):
  
    bvalue,svalue,r1value,r2value,s1value,s2value,buytarget1,selltarget1=gannsquare(data['close'][1])
    if abs(data['close'][1]-bvalue)>abs(data['close'][1]-svalue) and abs(data['close'][1]-svalue)<=1 :
        gannpostiondata='up'
    elif abs(data['close'][1]-bvalue)<abs(data['close'][1]-svalue) and abs(data['close'][1]-bvalue)<=1:
        gannpostiondata='down'
    else:
        gannpostiondata='no'
   

    return gannpostiondata
    


def get_openposition(open_position,start_price,risk,reward,data):
    try:
        low_price=data['low'].iloc[-1]
        high_price=data['high'].iloc[-1]
        postion_type=data['trigger_start'].iloc[-1]
        
        if postion_type==1:
            if  start_price-data['low'].iloc[-1]>= risk:
                open_position=0
                end_price=start_price-risk
                current_runn='stopped'
                trigger_start=3
                pnl= round(bottomline(start_price,end_price),2)
            
            elif data['high'].iloc[-1]-start_price>= reward:
                open_position=0
                end_price=start_price+reward
                current_runn='stopped'
                trigger_start=3
                pnl= round(bottomline(start_price,end_price),2)
                
            else:
                open_position=3
                end_price=0
                current_runn='waiting'
                trigger_start=data['trigger_start'].iloc[-1]
                pnl= 0.00
        

        elif postion_type==0:
            if  data['high'].iloc[-1]-start_price>=risk:
                open_position=0
                end_price=start_price+risk
                current_runn='stopped'
                trigger_start=3
                pnl= round(bottomline(end_price,start_price),2)
            
            
            
            elif start_price-data['low'].iloc[-1]>= reward:
                open_position=0
                end_price=start_price-reward
                current_runn='stopped'
                trigger_start=3
                pnl= round(bottomline(end_price,start_price),2)
                
        
            else:
                open_position=3
                end_price=0
                current_runn='waiting'
                trigger_start=data['trigger_start'].iloc[-1]
                pnl= 0.00
            
        else:
            end_price=0
            open_position=3
            current_runn='waiting'
            start_price=0
            trigger_start=data['trigger_start'].iloc[-1]
            pnl= 0.00
    except Exception as e:
        raise(e)
        print(e)
       
    return end_price,open_position,current_runn,start_price,trigger_start,pnl,risk,reward
   


def ema_strategy(data,open_position,start_price,risk,reward):
    latest_data =data.reset_index(drop=True)
    emaTrend=latest_data['ematrend'].iloc[-1]
    positiondata=gannposition(latest_data)
    if open_position==0.0 :
        bvalue,svalue,r1value,r2value,s1value,s2value,buytarget1,selltarget1=gannsquare(latest_data['close'].iloc[-1])
        
        pnl= 0.00
        #starting a signal
        if emaTrend=='up' :
            trigger_start=1#buy
            open_position=1
            current_runn='start'
            start_price=latest_data['close'].iloc[-1]
            end_price=0
            reward=round(abs(start_price-buytarget1),2)
            risk=reward/2
            # risk= now_price =latest_data['dL'][1]
        elif emaTrend=='down': 
            trigger_start=0#sell
            open_position=1
            current_runn='start'
            start_price=latest_data['close'].iloc[-1]
            end_price=0
            reward=round(abs(start_price-selltarget1),2)
            risk=reward/2
            # risk= now_price =latest_data['dH'][1]
        else: 
            trigger_start=3#sell
            open_position=0
            current_runn='waiting'
            start_price=0
            end_price=0
            risk= 0
            reward=0

       
    elif open_position==1 or open_position==3: 
       
        
        end_price,open_position,current_runn,start_price,trigger_start,pnl,risk,reward=get_openposition(open_position,start_price,4,7,latest_data)
    



    else:
        trigger_start=3#waiting3
        start_price=0
        end_price=0
        pnl= 0.00
        risk=0
        reward=0

    return trigger_start,open_position,current_runn,start_price,end_price,pnl,risk,reward

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







    

