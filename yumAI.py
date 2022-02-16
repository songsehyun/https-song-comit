import imp
import time
import pyupbit
import datetime
import schedule
from fbprophet import Prophet
import requests

access = "your-access"
secret = "your-secret"

def krw_ticker():
    url = "https://api.upbit.com/v1/market/all"
    resp= requests.get(url)
    data = resp.json()
    krw_ticker = []
    for coin in data:
        ticker = coin['market']
        if ticker.startswith("KRW"):
            krw_ticker.append(ticker)
            
    return krw_ticker


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances() #업비트 원화 잔고조회
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0 #잔고가 없으면 리턴0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

#AI 예측 코드
predicted_close_price = 0
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute60") #한시간 단위로 최근200시간 데이터를 가져옴
    df = df.reset_index()
    df['ds'] = df['index'] # 매시간 마다 나온 데이터를 가져옴
    df['y'] = df['close'] # 매시간 마다 종가를 데이터로 가져옴
    data = df[['ds','y']]
    model = Prophet()  #데이터를 학습 하는 과정1
    model.fit(data)    #데이터를 학습 하는 과정2
    future = model.make_future_dataframe(periods=24, freq='H') #24시간 미래를 예측하는 과정1
    forecast = model.predict(future)                           #24시간 미래를 예측하는 과정2
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue
predict_price("KRW-MANA")
schedule.every().hour.do(lambda: predict_price("KRW-MANA"))

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-MANA")
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-MANA", 0.5)
            current_price = get_current_price("KRW-MANA")
            if target_price < current_price and current_price < predicted_close_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-MANA", krw*0.9995)
        else:
            btc = get_balance("MANA")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-MANA", btc)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
