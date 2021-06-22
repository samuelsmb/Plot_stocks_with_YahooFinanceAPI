from Run import Run as R
import statistics
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from _datetime import datetime

class Strat:
    
    def __init__(self, instrument):
        self.instrument = instrument
        self.admin= R(instrument=self.instrument, fullPeriod=True, period='2y', interval='1d')
        
        self.admin.computeRSI()
        self.admin.BBI()
        self.admin.PCT_CHANGE()

        self.buyPositions = np.empty((0), float)
        self.sellPositions = np.empty((0), float)


    def MA50_100(self, show=False, tradingPower=10000):
        period50    = 50
        period100   = 100
        
        b = np.empty((0), int)
        s = np.empty((0), int)

        self.admin.df['CROSS_PCT'] = (  (self.admin.df['MA50'] - self.admin.df['MA100']) / self.admin.df['MA50']  ) * 100

        MAprofit = 0
        buy=0
        sell=0
        shares = tradingPower/float(self.admin.df['Close'].head(1))
        bought = True
        buy+=1
       
        for i in range (len(self.admin.df['CROSS_PCT'])):
            close = self.admin.df.iloc[i:i+1 ,[3]].values[0]
            value = self.admin.df.iloc[i:i+1 ,[12]].values[0]
            
            if value > 0 and bought == False:
                shares = (tradingPower/close)
                bought = True
                b = np.append(b, close)
                buy+=1
            elif value < 0 and bought == True:
                s = np.append(s, close)
                MAprofit += (shares * close) - tradingPower
                shares = 0
                bought = False
                sell+=1
        
        if shares > 0:
            MAprofit += (shares * self.admin.df['Close'].tail(1)) - tradingPower
            s = np.append(s, self.admin.df['Close'].tail(1))
            sell+=1
        
        self.buyPositions = np.append(self.buyPositions, b)
        self.sellPositions = np.append(self.sellPositions, s)

        # print("BUY: ", self.buyPositions)
        # print("SELL: ", self.sellPositions)
        # print("ACCOUNT: ", account)

        if (show):
            plt.figure()
            plt.plot((admin.admin.df['MA50']), color='green')
            plt.plot((admin.admin.df['MA100']), color='red')
            plt.plot(admin.admin.df['Close'], color='blue')


            plt.show()


        return (MAprofit - (buy+sell)*40)
                
    
    def MA20_50(self, show=False, tradingPower=10000):
        b = np.empty((0), int)
        s = np.empty((0), int)

        self.admin.df['CROSS_PCT'] = (  (self.admin.df['MA20'] - self.admin.df['MA50']) / self.admin.df['MA20']  ) * 100

        MAprofit = 0
        buy=0
        sell=0
        shares = tradingPower/float(self.admin.df['Close'].head(1))
        bought = True
        buy+=1
       
        for i in range (len(self.admin.df['CROSS_PCT'])):
            close = self.admin.df.iloc[i:i+1 ,[3]].values[0]
            value = self.admin.df.iloc[i:i+1 ,[12]].values[0]
            
            if value > 0 and bought == False:
                shares = (tradingPower/close)
                bought = True
                b = np.append(b, close)
                buy+=1
            elif value < 0 and bought == True:
                s = np.append(s, close)
                MAprofit += (shares * close) - tradingPower
                shares = 0
                bought = False
                sell+=1
        
        if shares > 0:
            MAprofit += (shares * self.admin.df['Close'].tail(1)) - tradingPower
            s = np.append(s, self.admin.df['Close'].tail(1))
            sell+=1
        
        self.buyPositions = np.append(self.buyPositions, b)
        self.sellPositions = np.append(self.sellPositions, s)

        if (show):
            plt.figure()
            plt.plot((admin.admin.df['MA20']), color='green')
            plt.plot((admin.admin.df['MA50']), color='red')
            plt.plot(admin.admin.df['Close'], color='blue')


            plt.show()
        
        return (MAprofit - (buy+sell)*40)

myPortfolioSP500 = list(('MSFT', 'AAPL', 'AMZN', 'FB', 'GOOGL', 'VZ', 'BRK-B'))

profit = 0
profitWithHold = 0

print("Start at:",  datetime.utcnow())
print("Starting Capital: 10000$")
for x in myPortfolioSP500:
    # print(x)
    admin = Strat(x)
    profit += float(admin.MA20_50(show=False, tradingPower=10000))
    profitWithHold += admin.admin.compareToHold()
print("\nProfit: ", profit + "$")
print("Profit with hold: ", profitWithHold + "$\n")
# print("Profit vs. profitWithHold: ", profit-profitWithHold)

print("Finished at: ", datetime.utcnow())


