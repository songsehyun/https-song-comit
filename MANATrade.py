#디센트럴랜드 트레이드
#하루하루 상승이 잘되는 장에서 유리함
import time
import pyupbit
import datetime

access = ""
secret = ""
coin="KRW-BTC"
coin_name="BTC"

def get_target_price1(ticker, k):
    """0900시 기준 변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price1 = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price1

def get_target_price2(ticker, k):
    """1000시 기준변동성 돌파 전략으로 매수 목표가 조회"""
    df=pyupbit.get_daily_ohlcv_from_base(ticker, base=10)
    target_price2 = df.iloc[-2]['close'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * k
    return target_price2

def get_target_price3(ticker, k):
    """1100시 기준변동성 돌파 전략으로 매수 목표가 조회"""
    df=pyupbit.get_daily_ohlcv_from_base(ticker, base=11)
    target_price3 = df.iloc[-2]['close'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * k
    return target_price3

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


a=int(0) 
b=int(0)
c=int(0)
'''여러번 매수를 방지하기 위한 변수'''
krw = (get_balance("KRW")/3)-0.0005  
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
            target_price1 = get_target_price1(coin, 0.5)
            current_price = get_current_price(coin)
            if krw > 5000 and target_price1 < current_price and a==0:
                upbit.buy_market_order(coin, krw)#- 매수
                a=int(1)
        else:
            btc = get_balance(coin_name)
            if btc > 0.00008 and a==1:
                upbit.sell_market_order(coin, btc)
                a=int(0)

        if start_time2 < now < end_time2 - datetime.timedelta(seconds=10): # 10시 
            target_price2 = get_target_price2(coin, 0.5)
            current_price = get_current_price(coin)
            if krw > 5000 and target_price2 < current_price and b==0:
                upbit.buy_market_order(coin, krw)#- 매수
                b=int(1)
        else:
            btc = get_balance(coin_name)
            if btc > 0.00008 and b==1:
                upbit.sell_market_order(coin, btc)#매도
                b=int(0)

        if start_time3 < now < end_time3 - datetime.timedelta(seconds=10): #11시
            target_price3 = get_target_price3(coin, 0.5)
            current_price = get_current_price(coin)
            if krw > 5000 and target_price3 < current_price and c==0:
                upbit.buy_market_order(coin, krw)#- 매수
                c=int(1)
        else:
            btc = get_balance(coin_name)
            if btc > 0.00008 and c==1:
                upbit.sell_market_order(coin, btc) #매도
                c=int(0)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
