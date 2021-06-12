import time
import pyupbit
import datetime
import requests
import telegram


#업비트 키
access = "gZQfwTcy5xx3YARQPGTT6jSIU7fKuBOAvvmk0aO2"
secret = "6ksKgmxJzpzjR1BsxTpEfmx7wif7XnSFXBIfORdd"


#텔레그램 메시지 전송을 위한 정보 
bot = telegram.Bot(token='1699282198:AAFt4sV3JbhXwk48wOPO5tpiNq-yYZLp9E0')
chat_id = 296456825




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

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=3)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

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
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 텔레그램 메시지 전송 
bot.sendMessage(chat_id=chat_id, text="자동매매 프로그램이 시작되었습니다. ")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-ETH", 0.5)
            ma15 = get_ma15("KRW-ETH")
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price: #and ma15 < current_price:이동평균 제외
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-ETH", krw*0.9995)
                    # 텔레그램 메시지 전송 
                    bot.sendMessage(chat_id=chat_id, text="BTC 샀어요!: "+ str(buy_result))
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                sell_result = upbit.sell_market_order("KRW-ETH", btc*0.9995)
                # 텔레그램 메시지 전송 
                bot.sendMessage(chat_id=chat_id, text="BTC 팔았어요!: "+ str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id=chat_id, text="아이쿠 오류가 발생했어요.")
        time.sleep(1)