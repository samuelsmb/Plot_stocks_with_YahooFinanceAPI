from datetime import datetime as dt
import datetime
import numpy
import yfinance as yf
import pandas as pd
from matplotlib import style, pyplot as plt
import math as m
import statistics


class Run():

    def __init__(self, instrument, year=dt.utcnow().strftime("%Y"), month= dt.utcnow().strftime("%m"), day=dt.utcnow().strftime("%d"), timedelta=1, fullPeriod=False, period='5y', interval='1d'):
        self.instrument    = instrument
        self.year          = int(year)
        self.month         = int(month)
        self.day           = int(day)
        self.start         = datetime.date(self.year, self.month, self.day)
        self.end           = self.start + datetime.timedelta(days=timedelta)

        self.fullPeriod    = fullPeriod
        self.period        = period
        self.interval      = interval
        self.df            = self.runYFINANCE()


    #Driver    
    def runYFINANCE(self):
        df = yf.Ticker(self.instrument)
        # boolean = self.fullPeriod

        if(self.fullPeriod):
            df = df.history(period=self.period, interval=self.interval)
            # df = numpy.array(df['Close'])
        else:
            df = df.history(interval='1m', start=str(self.start), end=str(self.end))
        
        arr = numpy.array(df)
        pdDF = pd.DataFrame(arr).drop([5, 6], axis=1)
        # pdDF = pd.DataFrame(arr)
        # pdDF = pd.DataFrame({'Open': df['Open'], 'High': df['High'], 'Low': df['Low'], 'Close': df['Close'], 'Volume': df['Volume']})
        pdDF.rename(columns={0: "Open", 1: "High", 2: "Low", 3:"Close", 4:"Volume"}, inplace=True)
        return pdDF


    def PCT_CHANGE(self):

        self.df['PCT_CHANGE'] = self.df['Close'].pct_change()*100
        self.df['PCT_CHANGE'].fillna(0, inplace=True)


    def computeRSI (self, time_window=14):
        
        arr = numpy.array(self.df['Close'].diff(1).dropna())
        diff = pd.DataFrame(arr) #data.diff(1).dropna()        # diff in one field(one day)

        # this preservers dimensions off diff values
        up_chg = 0 * diff
        down_chg = 0 * diff
        
        # up change is equal to the positive difference, otherwise equal to zero
        up_chg[diff > 0] = diff[ diff>0 ]
        
        # down change is equal to negative deifference, otherwise equal to zero
        down_chg[diff < 0] = diff[ diff < 0 ]
        
        up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
        down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
        
        rs = abs(up_chg_avg/down_chg_avg)
        rsi = 100 - 100/(1+rs)
        
        # print(diff.head())
        self.df['RSI'] = rsi
        # return rsi

    def BBI(self):

        #-------------------#
        period = 20
        multiplier = 2
        #-------------------#


        self.df['MA20'] = self.df['Close'].rolling(window=period).mean()
        self.df['MA50'] = self.df['Close'].rolling(window=50).mean()
        self.df['MA100'] = self.df['Close'].rolling(window=100).mean()

        self.df['UpperBand'] = self.df['Close'].rolling(period).mean() + self.df['Close'].rolling(period).std() * multiplier
        self.df['LowerBand'] = self.df['Close'].rolling(period).mean() - self.df['Close'].rolling(period).std() * multiplier

        # self.df['RSI'] = Run.computeRSI(self)
        # self.df['RSI'].fillna(0, inplace=True)
        # print( self.df['RSI'])
        # return self.df
    
    def bestFitLine(self, show=False):
        
        x = numpy.arange(len(self.df['Close']))
        y = numpy.array(self.df['Close'])
        close = numpy.array(self.df['Close'])

        m, b  = numpy.polyfit(x,y,deg=1)
        line  = (m * x) + b

        print (m, b)
        
        if (show):
            style.use('dark_background')
            plt.figure()
            plt.plot(line, 'r--')
            plt.plot(close, color='blue')

            plt.show()


    def compareToHold(self, tradingPower=10000, comission=40):
        start = self.df['Close'].head(1)
        end = self.df['Close'].tail(1)

        # print(self.admin.instrument, ": ", (float(end) / float(start)*tradingPower)- tradingPower)

        return (((float(end) / float(start)) * tradingPower) - 10000) -(comission*2) #Kurtasje


    def pltShow(self):
        
        Run.BBI(self)
        Run.PCT_CHANGE(self)

        maks = max(self.df['PCT_CHANGE'])
        minst = min(self.df['PCT_CHANGE'])
        # median = statistics.median(self.df['Close'])


        style.use('dark_background')

        #Plot percentage change
        plt.figure()
        plt.plot(self.df['PCT_CHANGE'], color="skyblue")
        plt.title(self.instrument + ' Percentage change')
        
        plt.axhline(maks*0.5, linestyle='--', color="red")
        plt.axhline(maks*0.75, linestyle='--', alpha=0.5, color="red")
        plt.axhline(minst*0.5, linestyle='--', color="green")
        plt.axhline(minst*0.75, linestyle='--', alpha=0.5, color="green")


        # plt.legend(loc=4)

        #Plot historical chart with bbi
        plt.figure()
        plt.plot(self.df['Close'], color="skyblue")
        plt.plot(self.df['UpperBand'], color="red")
        plt.plot(self.df['LowerBand'], color="green")
        plt.plot(self.df['MA20'], color="blue")
        plt.title(self.instrument + ' Historical Chart')
        # plt.axhline(median, linestyle='--', color="purple")

        # plt.legend(loc=4)

        #Plot RSI
        plt.figure()
        plt.xlabel('Date')
        plt.plot(self.df['RSI'], color="skyblue")
        plt.title(self.instrument + ' RSI chart')
        # plt.legend(loc=4)

        plt.axhline(0, linestyle='--', alpha=0.1)
        plt.axhline(20, linestyle='--', alpha=0.5, color="red")
        plt.axhline(30, linestyle='--', color="red")

        plt.axhline(70, linestyle='--', color="green")
        plt.axhline(80, linestyle='--', alpha=0.5, color="green")
        plt.axhline(100, linestyle='--', alpha=0.1)

        plt.show()

#Change ticker to any preferred stock. Find tickers here at: https://finance.yahoo.com/
#Example of plotting the Apple stock
# admin = Run("AAPL", fullPeriod=True, period='1mo', interval='1h')
# print(admin.computeRSI())
# admin.computeRSI()
# admin.BBI()
# admin.PCT_CHANGE()
# admin.pltShow()



#- AAPL: 1m data not available for startTime=1608588605 and endTime=1611267005. Only 7 days worth of 1m granularity data are allowed to be fetched per request.
# Parameters: 
# period : str Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max Either Use period parameter or 
# use start and end 
# interval : str Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo Intraday data cannot extend last 60 days 
