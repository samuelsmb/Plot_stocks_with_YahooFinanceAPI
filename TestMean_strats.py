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
    
    
 
    def meanStrat(self, tradingPower=10000):
        """
        Based upon finding the mean price of what a stock has been during a couple of days. If the price of that stock falls below
        this mean price, we will buy some stocks because we in theory can believe that the price will increase back to the mean price.
        
        However in this case we will sell them again at the moment the price of the stock can be sold for a profit. 
        Since we expect the price to rise again, we can asume that there is a fair chance of making a profit since the price should
        go up.
        """
        account = tradingPower
        shares = float()
        moneySpent = 0
        p = np.empty((0), int)
        bought = False
        targetPrice = float()


        for i in range(15, len(self.admin.df['Close'])):

            meanClose = statistics.mean(np.concatenate(self.admin.df.iloc[i-15:i ,[3]].values[0:15]))
            close = self.admin.df.iloc[i:i+1, [3]].values[0]

            if close < meanClose and bought == False:
                targetPrice = meanClose
                shares = tradingPower / close
                bought = True
                account -= tradingPower
            
            elif (close > targetPrice and bought == True):
                account+= (close*shares)
                shares=0
                bought=False
        
        return account[0]

if __name__ == '__main__':
    admin = Strat('AAPL')
    # print(admin.admin.df)
    profit = admin.meanStrat()
    profitWithHold = admin.admin.compareToHold()
    print("\nProfit with mean strategy: ", profit, "$")
    print("Profit with hold: ", profitWithHold, "$\n")