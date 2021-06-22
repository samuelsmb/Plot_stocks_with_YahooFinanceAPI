import numpy as np
from Run import Run as R
from matplotlib import pyplot as plt
from datetime import datetime
import threading
import pandas as pd

class Strat:
    
    def __init__(self, instrument):
        self.profit = 0
        self.instrument = instrument
        self.admin= R(instrument=self.instrument, fullPeriod=True, period='3mo', interval='1h')
        
        self.admin.BBI()
        self.admin.PCT_CHANGE()

        self.buyRegressionLines = np.empty((0), float)
        self.sellRegressionLines = np.empty((0), float)

    def LinearRegression1(self, interval, tradeSum=10000, comission=40):
        m = float()
        b = float()
        LRprofit = 0
        shares = 0
        buy=0
        sell=0


        shares = tradeSum/float(self.admin.df['Close'].head(1))
        bought = True
        buy+=1

        for i in range(interval, len(self.admin.df['Close'])):
            data = self.admin.df['Close'].iloc[i-interval:i].values[0:interval]
            close = self.admin.df['Close'].iloc[i:i+1].values[0]
            x = np.arange(len(data))
            y = np.array(data)

            m, b = np.polyfit(x, y, deg=1)
            line = (m * x) + b
            # print("Line."+ str(i) + ": ", line)

            if (m > 0 and bought == False):
                shares = tradeSum/close
                bought = True
                buy+=1

            elif (m < 0 and bought == True):
                LRprofit += (shares * close) - tradeSum
                shares = 0
                bought = False
                sell+=1

        if shares > 0:
            LRprofit += (shares * self.admin.df['Close'].tail(1)) - tradeSum
            sell+=1
        
        print("Len: ", len(self.admin.df), " ", self.instrument, "Buys: ", buy, "Sells: ", sell, "Total pris kurtasje: ", (buy+sell)*comission, "Profit eksl. kurtasje: ", LRprofit)
        return (LRprofit - ((buy+sell)*comission)) #kurtasje

    def LinearRegression2(self, interval, maxMoneyToSpend=10000, maxMoneyToSpendEachTrade=2000, comission=40):
        m = float()
        b = float()
        LRprofit = 0
        shares = 0
        buy=0
        sell=0
        moneySpent = 0

        shares += maxMoneyToSpendEachTrade/float(self.admin.df['Close'].head(1))
        moneySpent += maxMoneyToSpendEachTrade
        buy+=1

        for i in range(interval, len(self.admin.df['Close'])):
            data = self.admin.df['Close'].iloc[i-interval:i].values[0:interval]
            close = self.admin.df['Close'].iloc[i:i+1].values[0]
            x = np.arange(len(data))
            y = np.array(data)

            m, b = np.polyfit(x, y, deg=1)
            line = (m * x) + b
            # print("Line."+ str(i) + ": ", line)

            if (m > 0 and moneySpent < maxMoneyToSpend):
                shares += maxMoneyToSpendEachTrade/close
                moneySpent += maxMoneyToSpendEachTrade
                buy+=1

            elif (m < 0):
                sharesToSell = shares/5
                LRprofit += (sharesToSell * close) - (moneySpent/5)
                moneySpent -= (moneySpent/5)
                shares -= sharesToSell
                sell+=1

        if shares > 0:
            LRprofit += (shares * self.admin.df['Close'].tail(1)) - moneySpent
            sell+=1
        
        # print(self.admin.instrument, ": ", account)
        print("Len: ", len(self.admin.df), " ", self.instrument, "Buys: ", buy, "Sells: ", sell, "Total price of commisions: ", (buy+sell)*comission, "Profit excluding the commision: ", LRprofit)
        return (LRprofit - ((buy+sell)*comission)) #kurtasje
          
myPortfolioSP500 = list(('MSFT', 'AAPL', 'AMZN', 'FB', 'GOOGL', 'VZ', 'BRK-B'))

interval = 100
profit = 0
profitWithHold = 0

print("Started at:",  datetime.utcnow())

for x in myPortfolioSP500:
    # print(x)
    admin = Strat(x)
    profit += float(admin.LinearRegression2(interval=interval, maxMoneyToSpendEachTrade=5000, comission=10))
    profitWithHold += admin.admin.compareToHold(comission=10)

print("\nProfit: ", profit)
print("Profit with hold: ", profitWithHold, "\n")

print("Finished at: ", datetime.utcnow())


#Some testing with threads:
##########################Threads#################################

# print("Start at:",  datetime.utcnow())
# ts = list()

# for x in myPortfolioSP500:
#     admin = Strat(x)
#     t = threading.Thread(target=admin.LinearRegression(interval=interval))
#     ts.append(t)

# for t in ts:
#     t.start()

# for t in ts:
#     t.join()

# # print("Profit: ", profit)
# print("Finished at: ", datetime.utcnow())








