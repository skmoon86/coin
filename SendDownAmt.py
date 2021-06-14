import time
import pyupbit
import datetime
import requests
import telegram
import numpy as np


#업비트 키
access = "gZQfwTcy5xx3YARQPGTT6jSIU7fKuBOAvvmk0aO2"
secret = "6ksKgmxJzpzjR1BsxTpEfmx7wif7XnSFXBIfORdd"


#텔레그램 메시지 전송을 위한 정보 
bot = telegram.Bot(token='1699282198:AAFt4sV3JbhXwk48wOPO5tpiNq-yYZLp9E0')
chat_id = 296456825



CoinKind1 = "KRW-BTC"
#기준금액
StdAmt1 = 400000 # 40만원으로 함 

#코인종류 
CoinKind2 = "KRW-ETH"
#기준금액
StdAmt2 = 30000 # 3만원으로 함 


while True:
    df1 = pyupbit.get_ohlcv(CoinKind1, interval="minute15", count=3)
    df2 = pyupbit.get_ohlcv(CoinKind2, interval="minute15", count=3)

    #15분봉이 3연속 음봉인지 확인 
    df1['Diff'] = df1['open'] - df1['close']
    df1['IsMinus'] = np.where(df1['Diff'] > 0, 1, 0) #내려가면 1 아니면 0 

    
    df2['Diff'] = df2['open'] - df2['close']
    df2['IsMinus'] = np.where(df2['Diff'] > 0, 1, 0) #내려가면 1 아니면 0 

    #합계데이터만 있으면 됨.  
    dfSum1 = df1.sum()
    dfSum2 = df2.sum()

    IsMinus1 = dfSum1['IsMinus']
    SumAmt1 = dfSum1['Diff']

    IsMinus2 = dfSum2['IsMinus']
    SumAmt2 = dfSum2['Diff']

    if IsMinus1 == 3 and SumAmt1 > StdAmt1:
        # 텔레그램 메시지 전송 
        bot.sendMessage(chat_id=chat_id, text = CoinKind1 + " 하락 중. 누적 하락 액" + str(format(SumAmt1, ",")))
    
    if IsMinus2 == 3 and SumAmt2 > StdAmt1:
        # 텔레그램 메시지 전송 
        bot.sendMessage(chat_id=chat_id, text = CoinKind2 + " 하락 중. 누적 하락 액" + str(format(SumAmt2, ",")))

    time.sleep(300)
