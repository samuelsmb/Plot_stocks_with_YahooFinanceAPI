from Run import Run as R
import statistics
import numpy as np

class Strat:
    
    def __init__(self, instrument):
        self.instrument = instrument
        self.admin= R(instrument=self.instrument, fullPeriod=True)
        
        self.admin.BBI()
        self.admin.PCT_CHANGE()
        self.admin.computeRSI()

        self.holdingPositions = np.empty((0), float)

    def RSI_strat1(self, tradingpower=10000): # Buy the stock when the RSI level reaches or is above 65

        bought = False
        shares = float()
        account = tradingpower

        for i in range(21, len(self.admin.df['RSI'])):
            rsi = float(self.admin.df.iloc[i:i+1 ,[8]].values[0])
            price = float(self.admin.df.iloc[i:i+1 ,[3]].values[0])


            if rsi > 65 and bought == False:
                shares = 10000 / price

                account = account - 10000 - 80
                bought = True
                # holdingPositions = np.append(holdingPositions, price)

            if (rsi < 55 and bought == True):
                account = account + (  shares * price  ) - 80
                bought = False
    
        return account

    def RSI_strat2(self): #Buy the stock in multiple blocks while RSI shows momentum in the stock.

        # for i in range(len(admin.df['RSI'])):
        account = 100000
        shares = float()
        moneySpent = 0
        p = np.empty((0), int)


        for i in range(21, len(self.admin.df['RSI'])):
            rsi = float(self.admin.df.iloc[i:i+1 ,[8]].values[0]) #Få tak i verdien på kolonne 8 på gitt radintervall
            price = float(self.admin.df.iloc[i:i+1 ,[3]].values[0])


            if rsi > 45 and moneySpent < 9000:
                shares += 3000 / price

                account = account - 3000 #- 80
                p = np.append(p, price)

            if (rsi >= 65):
                account = account + (  shares * price  ) #- 80
                shares=0
    
        # print(p)
        self.holdingPositions = np.append(self.holdingPositions, p)
        print(self.holdingPositions)
        return account
    
    # We check what the mean RSI level has been during the last week and if the RSI_buy level now is higher or the same, we buy because we
    # believe that the momentum will continue to increase further until it reaches RSI_sell 
    def RSI_strat3(self, tradingpower=10000, RSI_buy=40, RSI_sell=60):  
        account = tradingpower
        shares = float()
        moneySpent = 0
        p = np.empty((0), int)
        bought = False


        for i in range(21, len(self.admin.df['RSI'])):
            rsiMeanBuy = statistics.median(np.concatenate(self.admin.df.iloc[i-5:i ,[8]].values[0:5]))
            rsiMeanSell = self.admin.df.iloc[i-1:i ,[8]].values[0]
            price = float(self.admin.df.iloc[i:i+1 ,[3]].values[0])


            if rsiMeanBuy < RSI_buy and bought == False and moneySpent<9000:
                shares = 3000 / price
                moneySpent+=3000
                account = account - 3000 #- 80
                p = np.append(p, price)
                bought = True

            if ((rsiMeanSell > RSI_sell) and bought == True):
                account = account + (  shares * price  ) #- 80
                shares=0
                bought = False
                moneySpent=0
    
        # print(p)
        self.holdingPositions = np.append(self.holdingPositions, p)
        print(self.holdingPositions)
        return account

    #If the RSI level is above the preferred value, we buy and sell as soon as the stock can be sold for profit.
    def RSI_strat4(self, tradingpower=10000, RSI_value=60): 

        account = tradingpower
        shares = float()
        moneySpent = 0
        p = np.empty((0), int)
        bought = False

        for i in range(21, len(self.admin.df['RSI'])):
            rsiMeanBuy = statistics.median(np.concatenate(self.admin.df.iloc[i-5:i ,[8]].values[0:5])) #Få tak i verdien på kolonne 8 på gitt radintervall
            rsi = self.admin.df.iloc[i:i+1, [8]].values[0]
            price = float(self.admin.df.iloc[i:i+1, [3]].values[0])

            if rsi > RSI_value and bought == False:
                shares = 10000/price
                account-=10000
                bought = True

            if (price * shares) > 10000 and bought == True:
                account+= (price*shares)
                bought = False
                shares = 0
        return account




#Example for Microsoft with strat 4:
admin = Strat('MSFT')
print("Account balance: ", admin.RSI_strat4())
# print(np.concatenate(admin.admin.df.iloc[21:31 ,[8]].values[0:12]))


