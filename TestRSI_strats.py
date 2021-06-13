from Run import Run as R
import statistics
import numpy as np

class Strat:
    
    def __init__(self, instrument):
        self.instrument = instrument
        self.admin= R(instrument=self.instrument, fullPeriod=True)
        
        self.admin.BBI()
        self.admin.PCT_CHANGE()

        self.holdingPositions = np.empty((0), float)

    def RSI_strat1(self): # kjøpe aksjer for 10 000 når rsi rsi har momentum på over 65

        # for i in range(len(admin.df['RSI'])):
        account = 100000
        bought = False
        shares = float()

        for i in range(21, len(self.admin.df['RSI'])):
            rsi = float(self.admin.df.iloc[i:i+1 ,[8]].values[0]) #Få tak i verdien på kolonne 8 på gitt radintervall
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

    def RSI_strat2(self): #Teori om å kjøpe litt og litt så lenge rsi har momentum

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
    
    def RSI_strat3(self): # baserer seg på å finne medianen over en aksjeuke og kjøpe dersom rsi innfylles for median

        # for i in range(len(admin.df['RSI'])):
        account = 100000
        shares = float()
        moneySpent = 0
        p = np.empty((0), int)
        bought = False


        for i in range(21, len(self.admin.df['RSI'])):
            rsiMeanBuy = statistics.median(np.concatenate(self.admin.df.iloc[i-5:i ,[8]].values[0:5])) #Få tak i verdien på kolonne 8 på gitt radintervall
            rsiMeanSell = self.admin.df.iloc[i-1:i ,[8]].values[0]
            price = float(self.admin.df.iloc[i:i+1 ,[3]].values[0])


            if rsiMeanBuy < 40 and bought == False and moneySpent<9000:
                shares = 3000 / price
                moneySpent+=3000
                account = account - 3000 #- 80
                p = np.append(p, price)
                bought = True

            if ((rsiMeanSell > 60) and bought == True):
                account = account + (  shares * price  ) #- 80
                shares=0
                bought = False
                moneySpent=0
    
        # print(p)
        self.holdingPositions = np.append(self.holdingPositions, p)
        print(self.holdingPositions)
        return account

    def RSI_strat4(self): #Når rsi er over 60 så selger vi med engang vi kan tjene penger på å selge

        account = 100000
        shares = float()
        moneySpent = 0
        p = np.empty((0), int)
        bought = False

        for i in range(21, len(self.admin.df['RSI'])):
            rsiMeanBuy = statistics.median(np.concatenate(self.admin.df.iloc[i-5:i ,[8]].values[0:5])) #Få tak i verdien på kolonne 8 på gitt radintervall
            rsi = self.admin.df.iloc[i:i+1, [8]].values[0]
            price = float(self.admin.df.iloc[i:i+1, [3]].values[0])

            if rsi > 60 and bought == False:
                shares = 10000/price
                account-=10000
                bought = True

            if (price * shares) > 10000 and bought == True:
                account+= (price*shares)
                bought = False
                shares = 0
        return account





admin = Strat('MSFT')
print(admin.RSI_strat4())
# print(np.concatenate(admin.admin.df.iloc[21:31 ,[8]].values[0:12]))


