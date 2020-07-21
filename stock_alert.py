from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import ta
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import smtplib
from ta.utils import dropna
import yfinance as yf
import sys
import time




# Get today's date as UTC timestamp
today = datetime.today().strftime("%d/%m/%Y")
today,tomonth,toyear = today.split("/")
today, tomonth, toyear = int(today), int(tomonth), int(toyear)

def get_data(ticker, timeframeyear):
    df = pdr.get_data_yahoo(symbols=ticker, start=datetime(toyear-timeframeyear, tomonth, today), 
                            end=datetime(toyear, tomonth, today))
    
    return df



def alert(ticker, period, interval):
    

    data = yf.Ticker(ticker).history(period=period, interval=interval)
    data = ta.add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")
    
    last = data.iloc[-1]
    sb = [ticker + ": "]
    send_alert = False
    
    if last["Close"] >= last["volatility_bbh"]:
        sb.append("\n")
        sb.append("above high bollinger band")
        send_alert = True
    if last["Close"] <= last["volatility_bbl"]:
        sb.append("\n")
        sb.append("above low bollinger band")
        send_alert = True
    if last["momentum_rsi"] >= 70:
        sb.append("\n")
        sb.append("above RSI")
        send_alert = True
    if last["momentum_rsi"] <= 30:
        sb.append("\n")
        sb.append("below RSI")
        send_alert = True
    if -0.1 <= last["trend_macd_diff"] <= 0.1:
        sb.append("\n")
        sb.append("MACD Convergence")
        send_alert = True
    
    
    print("_______________________________________")
    if send_alert:
        text = "".join(sb)
        print(text)
        return text
    else:
        sb.append("\n")
        sb.append("No alerts.")
        text = "".join(sb)
        print(text)
        return text




if __name__ == "__main__":


    period = sys.argv[1]
    interval = sys.argv[2]
    try:
        loop = bool(sys.argv[3])
    except:
        loop = False


    f = open("watch_list.txt", "r")
    watch_list = f.readlines()

    if loop:
        while True:
            body = ["Period: " + period + "; Interval: " + interval]

            for ticker in watch_list:
                ticker = ticker[:-1] if ticker[-1] == "\n" else ticker
                #use 1y, 1d  OR  5d, 1m
                body.append(alert(ticker,period=period, interval=interval))
            
                

            sent_from = ''
            to = [""]
            subject = 'Stock Alert'
            body = "\n_______________________________________\n".join(body)

            email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (sent_from, ", ".join(to), subject, body)


            gmail_user = ""
            gmail_password = ""

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()   # optional
            server.login(gmail_user,gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print('Email sent!')
            time.sleep(1800)
    else:
        


        body = ["Period: " + period + "; Interval: " + interval]

        for ticker in watch_list:
            ticker = ticker[:-1] if ticker[-1] == "\n" else ticker
            #use 1y, 1d  OR  5d, 1m
            body.append(alert(ticker,period=period, interval=interval))
        
            

        sent_from = ''
        to = [""]
        subject = 'Stock Alert'
        body = "\n_______________________________________\n".join(body)

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)


        gmail_user = ""
        gmail_password = ""

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()   # optional
        server.login(gmail_user,gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
