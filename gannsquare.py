
import pandas as pd
import math

def buyabove(data):
    if data[4][1]!='':
        bvalue=data[3][1]
        svalue=data[4][2]
        r1value=data[1][1]
        r2value=data[1][3]
        s1value=data[4][3]
        s2value=data[4][4]

    elif data[2][1]!='':
        bvalue=data[1][1]
        svalue=data[3][1]
        r1value=data[1][3]
        r2value=data[1][5]
        s1value=data[4][2]
        s2value=data[4][3]

    elif data[1][2]!='':
        bvalue=data[1][3]
        svalue=data[1][1]
        r1value=data[1][5]
        r2value=data[3][5]
        s1value=data[3][1]
        s2value=data[4][2]
    elif data[1][4]!='':
        bvalue=data[1][5]
        svalue=data[1][3]
        r1value=data[3][5]
        r2value=data[5][5]
        s1value=data[1][1]
        s2value=data[3][1]
    elif data[2][5]!='':
        bvalue=data[3][5]
        svalue=data[1][5]
        r1value=data[5][5]
        r2value=data[5][3]
        s1value=data[1][3]
        s2value=data[1][1]
    elif data[4][5]!='':
        bvalue=data[5][5]
        svalue=data[3][5]
        r1value=data[5][3]
        r2value=data[5][1]
        s1value=data[1][5]
        s2value=data[1][3]
    elif data[5][4]!='':
        bvalue=data[5][3]
        svalue=data[5][5]
        r1value=data[5][1]
        r2value=data[3][0]
        s1value=data[3][5]
        s2value=data[1][5]
    elif data[5][2]!='':
        bvalue=data[5][1]
        svalue=data[5][3]
        r1value=data[3][0]
        r2value=data[0][0]
        s1value=data[5][5]
        s2value=data[3][5]
    elif data[5][0]!='':
        bvalue=data[3][0]
        svalue=data[5][1]
        r1value=data[0][0]
        r2value=data[0][3]
        s1value=data[5][3]
        s2value=data[5][5]
    elif data[2][0]!='':
        bvalue=data[0][0]
        svalue=data[3][0]
        r1value=data[0][3]
        r2value=data[0][6]
        s1value=data[5][1]
        s2value=data[5][3]
    elif data[0][1]!='':
        bvalue=data[0][3]
        svalue=data[0][0]
        r1value=data[0][6]
        r2value=data[3][6]
        s1value=data[3][0]
        s2value=data[5][1]
    elif data[0][4]!='':
        bvalue=data[0][6]
        svalue=data[0][3]
        r1value=data[3][6]
        r2value=data[6][6]
        s1value=data[0][0]
        s2value=data[3][0]
    elif data[1][6]!='':
        bvalue=data[3][6]
        svalue=data[0][6]
        r1value=data[6][6]
        r2value=data[6][3]
        s1value=data[0][3]
        s2value=data[0][0]
    elif data[4][6]!='':
        bvalue=data[6][6]
        svalue=data[3][6]
        r1value=data[6][3]
        r2value=data[6][0]
        s1value=data[0][6]
        s2value=data[0][3]
    elif data[6][5]!='':
        bvalue=data[6][3]
        svalue=data[6][6]
        r1value=data[6][0]
        r2value=data[6][0]
        s1value=data[3][6]
        s2value=data[0][6]
    elif data[6][2]!='':
        bvalue=data[6][0]
        svalue=data[6][3]
        r1value=data[6][0]
        r2value=data[6][0]
        s1value=data[6][6]
        s2value=data[3][6]
    else:
        bvalue=0
        svalue=0
        r1value=0
        r2value=0
        s1value=0
        s2value=0

    
    buytarget1=round(r1value*0.9995,2)
    selltarget1=round(s1value*1.0005,2)

    
    return bvalue,svalue,r1value,r2value,s1value,s2value,buytarget1,selltarget1









def gannsquare(datapoint):
    ## getting intial values
    a=round(datapoint ** 0.5,2)
    #b value
    if isinstance(a, int):
        b=a+1
    else:
        b= math.ceil(a)
    c= math.floor(a)
    d=c-1
    ## setting up the square

    ganndataframe=pd.DataFrame(columns = [0,1,2,3,4,5,6], index = [0,1,2,3,4,5,6])
    ganndataframe.at[3,3]=round(d ** 2,2)
    ganndataframe.at[4,3]=round((d+0.875) ** 2,2)
    ganndataframe.at[5,3]=round((c+0.875) ** 2,2)
    ganndataframe.at[6,3]=round((b+0.875) ** 2,2)
    ganndataframe.at[2,3]=round((d+0.375) ** 2,2)
    ganndataframe.at[1,3]=round((c+0.375) ** 2,2)
    ganndataframe.at[0,3]=round((b+0.375) ** 2,2)
    # 3 series
    ganndataframe.at[3,6]=round((b+0.625) ** 2,2)
    ganndataframe.at[3,5]=round((c+0.625) ** 2,2)
    ganndataframe.at[3,4]=round((d+0.625) ** 2,2)
    ganndataframe.at[3,2]=round((d+0.125) ** 2,2)
    ganndataframe.at[3,1]=round((c+0.125) ** 2,2)
    ganndataframe.at[3,0]=round((b+0.125) ** 2,2)
    #cross series of
    ganndataframe.at[2,2]=round((d+0.25) ** 2,2)
    ganndataframe.at[2,4]=round((d+0.5) ** 2,2)
    ganndataframe.at[1,1]=round((c+0.25) ** 2,2)
    ganndataframe.at[0,0]=round((b+0.25) ** 2,2)
    ganndataframe.at[1,5]=round((c+0.5) ** 2,2)
    ganndataframe.at[0,6]=round((b+0.5) ** 2,2)
    ganndataframe.at[4,2]=round((d+1) ** 2,2)
    ganndataframe.at[5,1]=round((c+1) ** 2,2)
    ganndataframe.at[6,0]=round((b+1) ** 2,2)
    ganndataframe.at[4,4]=round((d+0.75) ** 2,2)
    ganndataframe.at[5,5]=round((c+0.75) ** 2,2)
    ganndataframe.at[6,6]=round((b+0.75) ** 2,2)
    # rest
    if datapoint>=ganndataframe.at[0,0] and datapoint<ganndataframe.at[0,6]:
        ganndataframe.at[0,1]=datapoint
    else:
        ganndataframe.at[0,1]=''
    if datapoint>=ganndataframe.at[0,3] and datapoint<ganndataframe.at[0,6]:
        ganndataframe.at[0,4]=datapoint
    else:
        ganndataframe.at[0,4]=''
    
    if datapoint>=ganndataframe.at[1,1] and datapoint<ganndataframe.at[1,3]:
        ganndataframe.at[1,2]=datapoint
    else:
        ganndataframe.at[1,2]=''

    if datapoint>=ganndataframe.at[1,3] and datapoint<ganndataframe.at[1,5]:
        ganndataframe.at[1,4]=datapoint
    else:
        ganndataframe.at[1,4]=''
        
    if datapoint>=ganndataframe.at[0,6] and datapoint<ganndataframe.at[3,6]:
        ganndataframe.at[1,6]=datapoint
    else:
        ganndataframe.at[1,6]=''
    
        
    if datapoint>=ganndataframe.at[3,0] and datapoint<ganndataframe.at[6,0]:
        ganndataframe.at[2,0]=datapoint
    else:
        ganndataframe.at[2,0]=''
           
    if datapoint>=ganndataframe.at[3,1] and datapoint<ganndataframe.at[1,1]:
        ganndataframe.at[2,1]=datapoint
    else:
        ganndataframe.at[2,1]=''
    
    if datapoint>=ganndataframe.at[1,5] and datapoint<ganndataframe.at[3,5]:
        ganndataframe.at[2,5]=datapoint
    else:
        ganndataframe.at[2,5]=''
    
    if datapoint>=ganndataframe.at[4,2] and datapoint<ganndataframe.at[3,1]:
        ganndataframe.at[4,1]=datapoint
    else:
        ganndataframe.at[4,1]=''
        
    if datapoint>=ganndataframe.at[3,5] and datapoint<ganndataframe.at[5,5]:
        ganndataframe.at[4,5]=datapoint
    else:
        ganndataframe.at[4,5]=''
    
        
    if datapoint>=ganndataframe.at[3,6] and datapoint<ganndataframe.at[6,6]:
        ganndataframe.at[4,6]=datapoint
    else:
        ganndataframe.at[4,6]=''
    
         
    if datapoint>=ganndataframe.at[5,1] and datapoint<ganndataframe.at[3,0]:
        ganndataframe.at[5,0]=datapoint
    else:
        ganndataframe.at[5,0]=''
         
    if datapoint>=ganndataframe.at[5,3] and datapoint<ganndataframe.at[5,1]:
        ganndataframe.at[5,2]=datapoint
    else:
        ganndataframe.at[5,2]=''
    
    if datapoint>=ganndataframe.at[5,5] and datapoint<ganndataframe.at[5,3]:
        ganndataframe.at[5,4]=datapoint
    else:
        ganndataframe.at[5,4]=''

    
    if datapoint>=ganndataframe.at[6,3] and datapoint<ganndataframe.at[6,0]:
        ganndataframe.at[6,2]=datapoint
    else:
        ganndataframe.at[6,2]=''

    if datapoint>=ganndataframe.at[6,6] and datapoint<ganndataframe.at[6,3]:
        ganndataframe.at[6,5]=datapoint
    else:
        ganndataframe.at[6,5]=''
    
    ganndataframe=ganndataframe.fillna('')
   
    ganndataframe=ganndataframe.T
  

    bvalue,svalue,r1value,r2value,s1value,s2value,buytarget1,selltarget1=buyabove(ganndataframe)
    return bvalue,svalue,r1value,r2value,s1value,s2value,buytarget1,selltarget1

    
    

  