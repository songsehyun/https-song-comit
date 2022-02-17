#디센트럴랜드 트레이드
import time
import pyupbit
import datetime

access = ""
secret = ""
coin="KRW-MANA"
coin_name="MANA"
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
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time1 = get_start_time(coin) 
        start_time2 = start_time1 + datetime.timedelta(minutes=60)
        start_time3 = start_time1 + datetime.timedelta(minutes=120)
        end_time1 = start_time1 + datetime.timedelta(days=1)
        end_time2 = start_time2 + datetime.timedelta(days=1)
        end_time3 = start_time3 + datetime.timedelta(days=1)
        #0900i 부터 0859:50i
        if start_time1 < now < end_time1 - datetime.timedelta(seconds=10): #9시
            target_price = get_target_price(coin, 0.5)
            current_price = get_current_price(coin)
            if target_price < current_price: 
                krw = get_balance("KRW")     
                if krw > 5000:
                    upbit.buy_market_order(coin, krw*0.1999)#- 매수
        else:
            btc = get_balance(coin_name)
            if btc > 0.00008:
                upbit.sell_market_order(coin, btc)

        if start_time2 < now < end_time2 - datetime.timedelta(seconds=10): # 10시 
            target_price = get_target_price(coin, 0.5)
            current_price = get_current_price(coin)#매도
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order(coin, krw*0.1999)#- 매수
        else:
            btc = get_balance(coin_name)
            if btc > 0.00008:
                upbit.sell_market_order(coin, btc)#매도

        if start_time3 < now < end_time3 - datetime.timedelta(seconds=10): #11시
            target_price = get_target_price(coin, 0.5)
            current_price = get_current_price(coin)
            if target_price < current_price:
                krw = get_balance("KRW")    
                if krw > 5000:
                    upbit.buy_market_order(coin, krw*0.1999)#- 매수
        else:
            btc = get_balance(coin_name)
            if btc > 0.00008:
                upbit.sell_market_order(coin, btc) #매도

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)