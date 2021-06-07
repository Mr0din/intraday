
import pandas as pd
from tikrdata import get_livequote
import math
import numpy as np
from tqdm import tqdm

def bottomline(buyprice,sellprice):
    no_of_shares=round(150000/buyprice)
    turnaround=no_of_shares*(buyprice+sellprice)
    brokerage= 20
    stt= round((sellprice*no_of_shares)*0.00025)
    tc=round(turnaround*0.0000325,2)
    gst=round(0.18*(brokerage+tc),2)
    sebi=round(0.000001*turnaround,2)
    stamp=round(0.000002*turnaround,2)
    total=brokerage+stt+tc+gst+sebi+stamp
    bottomline=(sellprice-buyprice)*no_of_shares - total
    # print('Prift or loss:',bottomline)
    return bottomline



def equityMomentum(data,uiquedatelist):
    total_data=pd.DataFrame()
    count=0
    
    dataframe1= pd.DataFrame()
    
    for c,i in tqdm(enumerate(uiquedatelist)):

        if c==len(uiquedatelist)-1 or c<=2:
            pass
        else:
            new_data=data[data['Date']==i] 
            new_data1=data[data['Date']==uiquedatelist[c-1]] 
            new_data2=data[data['Date']==uiquedatelist[c-2]] 
            new_data3=data[data['Date']==uiquedatelist[c-3]]
            new_data4=data[data['Date']==uiquedatelist[c+1]]
            
            new_data=new_data.reset_index(drop=True)
            new_data1=new_data1.reset_index(drop=True)
            new_data2=new_data2.reset_index(drop=True)
            new_data3=new_data3.reset_index(drop=True)
            new_data4=new_data4.reset_index(drop=True)
            # new_data5=new_data5.reset_index(drop=True)
            # new_data.to_csv('newsdata.csv')
            # new_data1.to_csv('newsdata1.csv')
            # new_data2.to_csv('newsdata2.csv')
            # new_data3.to_csv('newsdata3.csv')
            # new_data4.to_csv('newsdata4.csv')
            # break
    

    
            if c <=2 :
                intermediate=pd.DataFrame()
                pass
            else:
                intermediate=pd.DataFrame()
                uniquetikr= set(list(new_data['tikr']))
                uniquetikr=list(uniquetikr)
                for count,tikr in enumerate(uniquetikr):
                    
                   
                    perchange3=round((new_data['close'][count]-new_data1['close'][count])/new_data1['close'][count],5)
                    perchange2=round((new_data1['close'][count]-new_data2['close'][count])/new_data2['close'][count],5)
                    perchange1=round((new_data2['close'][count]-new_data3['close'][count])/new_data3['close'][count],5)
                    # volchange1= round((new_data1['volume'][count]-new_data2['volume'][count])/new_data2['volume'][count],5)
                    # volchange2= round((new_data2['volume'][count]-new_data3['volume'][count])/new_data3['volume'][count],5)
                    # highchange1= round((new_data1['open'][count]-new_data2['open'][count])/new_data2['open'][count],5)
                    # highchange2= round((new_data2['open'][count]-new_data3['open'][count])/new_data3['open'][count],5)
                    if perchange3>perchange2>perchange1 and perchange3>0 and perchange1>0:

                        # print('----------------------------------------------------------------')
                        # print(new_data4['open'][count],new_data4['Date'][count+1] )
                        # print(new_data['close'][count],new_data['Date'][count] )
                        # print(new_data1['close'][count], new_data1['Date'][count])
                        # print(new_data2['close'][count], new_data2['Date'][count])
                        # # print(new_data3['close'][count], new_data3['Date'][count])
                        # print('----------------------------------------------------------------')

                        
                        intermediate.at[count,'tikr']=new_data['tikr'][count]
                        intermediate.at[count,'entrydate']=i
                        intermediate.at[count,'exitdate']=uiquedatelist[c+1]
                        intermediate.at[count,'change1']=round(perchange3,5)
                        intermediate.at[count,'change0']=round(perchange2,5)
                        intermediate.at[count,'totalchange']=round(round(perchange3,5)+round(perchange2,5)+round(perchange1,5),5)
                        intermediate.at[count,'changediff']=round(round(perchange3,5)-round(perchange2,5),5)
                        intermediate.at[count,'entry']=new_data['close'][count]
                        intermediate.at[count,'exit']=new_data4['open'][count]
                        pnl=bottomline(intermediate['entry'][count],intermediate['exit'][count])
                        

                        # if new_data['close'][count]+0.02*new_data['close'][count]<=new_data4['high'][count]:
                        #     intermediate.at[count,'entry']=new_data['close'][count]
                        #     intermediate.at[count,'exit']=new_data['close'][count]+0.02*new_data['close'][count]
                        #     intermediate.at[count,'touchedlow']=1
                        #     pnl=bottomline(intermediate['entry'][count],intermediate['exit'][count])
                        #     intermediate.at[count,'totalchange']=round(round(perchange3,5)+round(perchange2,5),5)
                        #     intermediate.at[count,'changediff']=round(round(perchange3,5)-round(perchange2,5),5)
                        # elif new_data['close'][count]+0.02*new_data['close'][count]<=new_data4['high'][count]
                        #     intermediate.at[count,'entry']=new_data['close'][count]
                        #     intermediate.at[count,'exit']=new_data['high'][count]
                        #     pnl=bottomline(intermediate['entry'][count],intermediate['exit'][count])
                        #     intermediate.at[count,'touchedlow']=0
                        #     intermediate.at[count,'totalchange']=round(round(perchange3,5)+round(perchange2,5),5)
                        #     intermediate.at[count,'changediff']=round(round(perchange3,5)-round(perchange2,5),5)
                            
                            
                        intermediate.at[count,'pnl']=round(pnl,2)
                        # total_data=total_data.append(intermediate)

                    else:
                        pass
                
                if intermediate.empty:
                    final_intermediate=pd.DataFrame()
                else:
                    # intermediate.to_csv('intermediate.csv')
                    
                    # intermediate=intermediate[intermediate['touchedlow']==1]
                    intermediate.to_csv('intermediate.csv')
                   
                    
                    intermediate=intermediate.reset_index(drop=True)
                    if list(intermediate['change1'])==[]:
                        final_intermediate=pd.DataFrame()
                        pass  
                    else:
                        max_number =max(list(intermediate['change1']))
                        row_value= list(intermediate['change1']).index(float(max_number))
                        final_intermediate=intermediate.loc[[row_value]]
                    dataframe1=dataframe1.append(final_intermediate)
        
                      
              
       
    

    return dataframe1






def backtestStrategy_live(tikrname,strategytimeline):
    data=get_livequote(tikrname, strategytimeline,'1d')
    data=data.reset_index()
    dataframe=equityMomentum(data)
    return dataframe
    



def main():
    dataframe= pd.read_csv('data6m.csv')
    uniquedate=set(list(dataframe['Date']))
    uniquedate=sorted(list(uniquedate))
    finaldata=equityMomentum(dataframe,uniquedate)
    finaldata.to_csv('equitydata.csv')
    
    
### data collection    
# listofstocks=['AARTIIND.NS','ACC.NS','ADANIENT.NS','ADANIPORTS.NS','ALKEM.NS','AMARAJABAT.NS','APLLTD.NS','AMBUJACEM.NS','APOLLOHOSP.NS','APOLLOTYRE.NS','ASHOKLEY.NS','ASIANPAINT.NS','AUBANK.NS','AUROPHARMA.NS','AXISBANK.NS','BAJAJ-AUTO.NS','BAJAJFINSV.NS','BAJFINANCE.NS','BANDHANBNK.NS','BALKRISIND.NS','BANKBARODA.NS','BATAINDIA.NS','BEL.NS','BERGEPAINT.NS','BHARATFORG.NS','BHARTIARTL.NS','BHEL.NS','BIOCON.NS','BOSCHLTD.NS','BPCL.NS','BRITANNIA.NS','CADILAHC.NS','CANBK.NS','CHOLAFIN.NS','CIPLA.NS','COALINDIA.NS','COFORGE.NS','COLPAL.NS','CONCOR.NS','CUB.NS','CUMMINSIND.NS','DABUR.NS','DEEPAKNTR.NS','DIVISLAB.NS','DLF.NS','DRREDDY.NS','EICHERMOT.NS','ESCORTS.NS','EXIDEIND.NS','FEDERALBNK.NS','GAIL.NS','GLENMARK.NS','GMRINFRA.NS','GODREJCP.NS','GODREJPROP.NS','GRANULES.NS','GRASIM.NS','GUJGASLTD.NS','HAVELLS.NS','HCLTECH.NS','HDFC.NS','HDFCAMC.NS','HDFCBANK.NS','HDFCLIFE.NS','HEROMOTOCO.NS','HINDALCO.NS','HINDPETRO.NS','HINDUNILVR.NS','IBULHSGFIN.NS','ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','IDEA.NS','IDFCFIRSTB.NS','IGL.NS','INDIGO.NS','INDUSINDBK.NS','INFY.NS','INDUSTOWER.NS','IOC.NS','IRCTC.NS','ITC.NS','JINDALSTEL.NS','JSWSTEEL.NS','KOTAKBANK.NS','JUBLFOOD.NS','LALPATHLAB.NS','L&TFH.NS','LT.NS','LICHSGFIN.NS','LTTS.NS','LTI.NS','M&M.NS','LUPIN.NS','M&MFIN.NS','MFSL.NS','MCDOWELL-N.NS','MARICO.NS','MARICO.NS','MANAPPURAM.NS','MARUTI.NS','MUTHOOTFIN.NS','MPHASIS.NS','MOTHERSUMI.NS','MINDTREE.NS','MGL.NS','MRF.NS','ONGC.NS','NTPC.NS','NMDC.NS','NESTLEIND.NS','NAUKRI.NS','NATIONALUM.NS','NAM-INDIA.NS','NAVINFLUOR.NS','PIDILITIND.NS','PFIZER.NS','PFC.NS','PETRONET.NS','PAGEIND.NS','PAGEIND.NS','PEL.NS','RELIANCE.NS','RECLTD.NS','RBLBANK.NS','RAMCOCEM.NS','PVR.NS','POWERGRID.NS','PNB.NS','PIIND.NS','SUNPHARMA.NS','SRTRANSFIN.NS','SRF.NS','SIEMENS.NS','SHREECEM.NS','SBILIFE.NS','SBILIFE.NS','SAIL.NS','SBIN.NS','TATACHEM.NS','SUNTV.NS','TRENT.NS','TORNTPOWER.NS','TORNTPHARM.NS','TITAN.NS','TECHM.NS','TCS.NS','TATASTEEL.NS','TATAPOWER.NS','TATAMOTORS.NS','TATACONSUM.NS','ZEEL.NS','VEDL.NS','UPL.NS','ULTRACEMCO.NS','UBL.NS','TVSMOTOR.NS','TVSMOTOR.NS','WIPRO.NS','VOLTAS.NS']
# def datacollect():
#     final_df=pd.DataFrame()
#     for i in tqdm(listofstocks):
#         data=get_livequote(i, '6mo','1d')
#         final_df=final_df.append(data)

#     final_df.to_csv('data6m.csv')

# datacollect()

main()
