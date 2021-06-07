import yfinance as yf
import pandas as pd
from pymongo import MongoClient


def get_livequote(sym, period,interval):
    tickers = yf.Ticker(sym)
    dataframe_=tickers.history(period=period, interval=interval,actions=False)

    ##rename the columns    
    df = dataframe_.rename(columns={ 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})

    df['tikr']=sym
 
    df.sort_index(inplace=True)
    ##extract the columns you want
    df = df[['tikr','open', 'high', 'low', 'close', 'volume']]

    return df
# print(get_quote('^STI','10y', '1d'))


def ConnectProd(db):
    MONGO_URI = "mongodb://192.168.0.6:27017"
    client = MongoClient(MONGO_URI)
    mdb=client[db]
    return mdb,client
  

def get_niftydata():
    mdb,client=ConnectProd('market')
    data=mdb["nifty_data"].find({})
    data=list(data)
    client.close()
    data= pd.DataFrame(data)
    data=data.drop(['_id','extra'],axis=1)
    print(data)
    # return data

def get_techindicator(data):
    data['H-L'] = data['high'] - data['low']
    data['O-C'] = data['close'] - data['open']
    data['SMA'] = trend.sma_indicator(data["close"], n=60, fillna=True)
    data["EMA"]=trend.ema_indicator(data["close"], n=60, fillna=True)
    data["KAMA"]=momentum.kama(data["close"], n=60, pow1=60, pow2=60, fillna=True)
    data["MACD"]=round(trend.macd(data["close"], n_fast=12, n_slow=26, fillna=True),5)
    data["MACDEXT"]=trend.macd_diff(data["close"], n_fast=12, n_slow=26, n_sign=9, fillna=True)
    data["STOCH"]=momentum.stoch(data["high"], data["low"], data["close"], n=14, fillna=True)
    data["RSI"]=momentum.rsi(data["close"], n=60, fillna=True)
    data["ADX"]=trend.adx(data["high"], data["low"], data["close"], n=60, fillna=True)
    data["CCI"]=trend.cci(data["high"], data["low"], data["close"], n=60, c=0.015, fillna=True)
    data["AROONUP"]=trend.aroon_up(data["close"], n=60, fillna=True)
    data["AROONDOWN"]=trend.aroon_down(data["close"], n=60, fillna=True)
    data["MSI"]=volume.money_flow_index(data["high"], data["low"], data["close"], data["volume"], n=60, fillna=True)
    data["TRIX"]=trend.trix(data["close"], n=60, fillna=True)
    data["BBANDSHIGH"]=volatility.bollinger_hband(data["close"], n=60, ndev=2, fillna=True)
    data["BBANDSLOW"]=volatility.bollinger_lband(data["close"], n=60, ndev=2, fillna=True)
    data["ATR"]=volatility.average_true_range(data["high"], data["low"], data["close"], n=60, fillna=True)
    data["AD"]=volume.chaikin_money_flow(data["high"], data["low"], data["close"], data["volume"], n=60, fillna=True)
    data["OBV"]=volume.on_balance_volume(data["close"], data["volume"], fillna=True)
    data["WILLR"]=momentum.wr(data["high"], data["low"], data["close"], lbp=60, fillna=True)

    # New Indicators 
    # 1 Mometum indicartors
    data['awesome_oscialltor']=momentum.ao(data['high'], data['low'], 5, 34, False)
    data['kama_indicator']=momentum.kama(data['close'], 10, 2, 30, False)
    data['rate_of_change']=momentum.roc(data['close'], 12, False)
    data['stoch_signal']=momentum.stoch_signal(data['high'], data['low'], data['close'], n=14, d_n=5, fillna=False)
    data['tsi']=momentum.tsi(data['close'], 25, 13, False)
    data['uo']=momentum.uo(data['high'], data['low'], data['close'],7, 14, 28, 4.0,2.0,  1.0, False)
    #2 volume indicators
    # data['adi']=volume.acc_dist_index(data["high"],data["low"], data["close"], data["volume"], fillna=False)
    # data['chaikin']=volume.chaikin_money_flow(data['high'], data['low'], data['close'], data['volume'], n=20, fillna=False)
    # data['emv']=volume.ease_of_movement(data["high"],data["low"], data["volume"], n=14, fillna=False)
    # data['force_index']=volume.force_index(data['close'], data['volume'], n=13, fillna=False)
    # data['nvi']=volume.negative_volume_index(data['close'], data['volume'], fillna=False)
    # data['vpt']=volume.volume_price_trend(data['close'], data['volume'], fillna=False)
    # 3  Volatility Trends
    data['bbands_high_indicator']=round(volatility.bollinger_hband_indicator(data['close'], n=20, ndev=2, fillna=False),4)
    data['bbands_low_indicator']=round(volatility.bollinger_lband_indicator(data['close'], n=20, ndev=2, fillna=False),4)
    data['bband_avg']=volatility.bollinger_mavg(data['close'], n=20, fillna=False)
    data['bband_percentage']=volatility.bollinger_pband(data['close'], n=40, ndev=2, fillna=False)
    data['bband_width']=volatility.bollinger_wband(data['close'], n=20, ndev=2, fillna=False)
    data['dc']=volatility.donchian_channel_hband(data['close'], n=20, fillna=False)
    data['dc_hban']=volatility.donchian_channel_hband_indicator(data['close'], n=20, fillna=False)
    data['dc_lband']=volatility.donchian_channel_lband(data['close'], n=20, fillna=False)
    data['dc_lband_indicator']=volatility.donchian_channel_lband_indicator(data['close'], n=20, fillna=False)
    data['kc_hband']=volatility.keltner_channel_hband(data['high'], data['low'], data['close'], n=10, fillna=False, ov=True)
    data['kc_hband_indicator']=volatility.keltner_channel_hband_indicator(data['high'], data['low'], data['close'], n=10, fillna=False, ov=True)
    data['kc_lband']=volatility.keltner_channel_lband(data['high'], data['low'], data['close'], n=10, fillna=False, ov=True)
    data['kc_lband_indicator']=volatility.keltner_channel_lband_indicator(data['high'], data['low'], data['close'], n=10, fillna=False, ov=True)
    data['kc_mband']=volatility.keltner_channel_mband(data['high'], data['low'], data['close'], n=10, fillna=False, ov=True)
    data['kc_pband']=volatility.keltner_channel_pband(data['high'], data['low'], data['close'], n=10, fillna=False, ov=True)
    data['kc_wband']=volatility.keltner_channel_pband(data['high'], data['low'], data['close'], n=10, fillna=False, ov=True)
    # Trend Indicator
    data['adx_negative']=trend.adx_neg(data['high'], data['low'], data['close'], n=14, fillna=False)
    data['adx_pos']= trend.adx_pos(data['high'], data['low'], data['close'], n=14, fillna=False)
    data['aroon_down']=trend.aroon_down(data['close'], n=25, fillna=False)
    data['aroon_up']=trend.aroon_up(data['close'], n=25, fillna=False)
    data['cci']=trend.cci(data['high'], data['low'], data['close'], n=20, c=0.015, fillna=False)
    data['dpo']=trend.dpo(data['close'], n=20, fillna=False)
    data['ema_indicator']=trend.ema_indicator(data['close'], n=12, fillna=False)
    data['ichimoku_a']=trend.ichimoku_a(data['high'], data['low'], n1=9, n2=26, visual=False, fillna=False)
    #data['ichimoku_b']=trend.ichimoku_b(data['high'], data['low'], n1=9, n2=26, visual=False, fillna=False)
    data['kst']=trend.kst(data['close'], r1=10, r2=15, r3=20, r4=30, n1=10, n2=10, n3=10, n4=15, fillna=False)
    data['kst_sig']=trend.kst_sig(data['close'], r1=10, r2=15, r3=20, r4=30, n1=10, n2=10, n3=10, n4=15, nsig=9, fillna=False)
    data['macd_signal']=round(trend.macd_signal(data['close'], n_slow=26, n_fast=12, n_sign=9, fillna=False),4)
    data['mass_index']=trend.mass_index(data['high'], data['low'], n=9, n2=25, fillna=False)
    data['pasr_down']=trend.psar_down(data['high'], data['low'], data['close'], step=0.02, max_step=0.2)
    data['psar_down_indicator']=trend.psar_down_indicator(data['high'], data['low'], data['close'], step=0.02, max_step=0.2)
    data['pasr_up']=trend.psar_up(data['high'], data['low'], data['close'], step=0.02, max_step=0.2)
    data['psar_down_indicator']=trend.psar_up_indicator(data['high'], data['low'], data['close'], step=0.02, max_step=0.2)
    data['trix']=trend.trix(data['close'], n=15, fillna=False)
    data['vortex_indicator_neg']=trend.vortex_indicator_neg(data['high'], data['low'], data['close'], n=14, fillna=False)
    data['vortex_indicator_pos']=trend.vortex_indicator_pos(data['high'], data['low'], data['close'], n=14, 
    fillna=False)
    data['future_close']=data['close'].shift(-1)
    return data


# def save_indb(data):

#     mdb['niftyexperiment'].insert_many()


