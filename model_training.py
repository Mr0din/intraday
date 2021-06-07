from tikrdata import get_livequote
import pandas as pd 
from pymongo import MongoClient
from tqdm import tqdm
import seaborn as sns 
import matplotlib.pyplot as plt 
from scipy.stats import norm 



def indices_correlation_stg():
    correlation_data=pd.DataFrame()
    indices=['^NSEI','^DJI','^IXIC','^N225','^HSI','^AXJO','^TWII','^STI','000001.SS','399001.SZ','^JKSE','^KS11','^GSPC','^DJI','^AORD','^KLSE','^XAX','^RUT','^GSPTSE','^FTSE','^GDAXI','^FCHI','^STOXX50E','^N100','^BFX','IMOEX.ME','^BVSP','^MXX','^IPSA','^MERV','^JN0U.JO','^NZ50']

    for i in tqdm(indices):
        total_data= get_livequote(i, '1y','1d')
        required_data= total_data[['close']]
        required_data=required_data.rename({"close": "close_"+i }, axis='columns')
        correlation_data=pd.concat([correlation_data, required_data], axis=1)
        # if i in []:
        #     #shifting forward
        # elif i in []:
        #     #shifting backward
        #     correlation_data=pd.concat([correlation_data, required_data], axis=1)
        # else:
        #     correlation_data=pd.concat([correlation_data, required_data], axis=1)



        column_means = correlation_data.mean()
        correlation_data = correlation_data.fillna(column_means)
       
    
#     # print(correlation_data)

    #correlation_data.to_csv('corr.csv')
    data=pd.read_csv('corr.csv' )
    corrmat = data.corr(method='pearson', min_periods=250) 
    corrmat.to_csv('correlation.csv')
    # f, ax = plt.subplots(figsize =(9, 8)) 
    # sns_plot=sns.heatmap(corrmat, ax = ax, cmap ="YlGnBu", linewidths = 0.1) 
    # sns_plot.figure.savefig("output.png")
   
# def get_trend(data):
#     for i in data.index:
#         if i > 0 :

           

def train_liearmodel():
    from keras.models import Sequential
    from keras.layers import Dense

    model = Sequential()
    model.add(Dense(64, input_shape=(10, ), activation='relu', name='dense_1'))
    model.add(Dense(64, activation='relu', name='dense_2'))
    model.add(Dense(64, activation='relu', name='dense_3'))
    model.add(Dense(64, activation='relu', name='dense_4'))
    model.add(Dense(1, activation='linear', name='dense_output'))
    model.compile(optimizer='adam', loss='mae', metrics=['mse'])
    
    return model

def train_data(data):
    from sklearn.decomposition import PCA
    pca=PCA(n_components=10)

    
    column_means = data.mean()
    data = data.fillna(column_means)
    from numpy import asarray
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train=data.drop(['close_^NSEI','Date'], axis=1)
    scaled = scaler.fit_transform(X_train)
    scaled=pca.fit_transform(scaled)
    print(scaled)
 
    y_train=data[['close_^NSEI']]
    y_train=y_train.values
  

    model=train_liearmodel()
    model.fit(scaled, y_train, epochs=1000, validation_split=0.05)
    return model
    
    

#train_data(pd.read_csv('corr.csv'))    



indices_correlation_stg()