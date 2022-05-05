"""
             _   _                   
            | | | |                  
   __ _ _ __| |_| |__  ___  ___  ___ 
  / _` | '__| __| '_ \/ __|/ _ \/ __|
 | (_| | |  | |_| | | \__ \  __/ (__ 
  \__,_|_|   \__|_| |_|___/\___|\___|
  Yuri Feitosa Negocio - yurinegocio@gmail.com

Its my python source code for Robin Hanson Logarithm Market Scoring Rule 
Several papers have explained this market maker, but the David Pennock post
is the best reference.

This implementation is only for fun and learn

url: http://blog.oddhead.com/2006/10/30/implementing-hansons-market-maker/
"""

from numpy import log as ln
from numpy import e
from math import ceil, floor
import numpy as np

class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

class LMSR(object):
    """
    The parameter “b” controls the maximum possible amount of money the market maker can lose 
    (which happens to be b*ln2 in the two-outcome case). The larger “b” is, the more money the 
    market maker can lose. But a larger “b” also means the market has more liquidity or depth, 
    meaning that traders can buy more shares at or near the current price without causing 
    massive price swings.
    """
    def __init__(self, b):
        self.b = b
    """
    The market maker also maintains a cost function C(q1,q2) which records how much money traders 
    have collectively spent so far, and depends only on the number of shares outstanding, q1 and q2
    For LMSR, the cost function is:
    """
    def C(self, q1, q2):
        return self.b*ln(e**(q1/self.b) + e**(q2/self.b))
    
    """
    The market maker uses the cost function to answer these questions. The cost to buy 13 shares of 
    outcome 1 is simply C(q1+13,q2) - C(q1,q2). The “cost” to sell 250 shares of outcome 2 
    is C(q1,q2-250) - C(q1,q2), which will be a negative number (negative cost), meaning that the seller 
    receives money in return for the shares. 
    """

    def cost_for_buy_yes(self, q1, q2, shares):
        return self.C(q1+shares,q2) - self.C(q1,q2)

    def payment_for_sell_yes(self, q1, q2, shares):
        return self.C(q1-shares,q2) - self.C(q1,q2)    

    def cost_for_buy_no(self, q1, q2, shares):
        return self.C(q1,q2+shares) - self.C(q1,q2)

    def payment_for_sell_no(self, q1, q2, shares):
        return self.C(q1,q2-shares) - self.C(q1,q2)   

    """
    If the market maker wants to quote a “current price”, he can. The current price for outcome 1 is:
    """
    def price(self,q1,q2):
        return e**(q1/self.b)/(e**(q1/self.b) + e**(q2/self.b))

    def price_yes(self,q1,q2):
        return self.price(q1,q2)

    def price_no(self,q1,q2):
        return self.price(q2,q1)
    """
    But note that the current price only applies for buying a miniscule (infinitesimal, in fact) number of shares. 
    As soon as a trader starts buying, the price immediately starts going up. In order to figure out the total cost 
    for buying some number of shares, we should use the cost function C, not the price function. 
    (If you remember your calculus: The total cost for buying k of shares of outcome 1 is the integral of the price 
    function from q1 to q1+k. The price function (“price1”) is the derivative of the cost function C with respect to q1, 
    and the cost function is the integral of the price function.)
    """


def main():
    print("Simulation")
    market = LMSR(100)
    
    """
    Here's a simple example. Suppose b=100 and no one has purchased any shares yet, so q1=q2=0.
    A trader arrives who wants to buy 10 shares of outcome 1. The trader must pay:
    C(10,0)-C(0,0) = 100 * ln(e10/100+e0) - 100 * ln(e0+e0) = $5.12
    """
    print ("The cost for buy 10 shares: " + bcolors.RED + str ( market.cost_for_buy_yes(0,0,10) ))

    """
    Now suppose that at some time later, the number of shares outstanding for outcome 1 is q1=50 
    and the number of shares outstanding of outcome 2 is q2=10. Now the same trader above returns 
    to the market and wants to sell her 10 shares. The trader's “payment” is:

    C(40,10)-C(50,10) = 100 * ln(e40/100+e10/100) - 100 * ln(e50/100+e10/100) = -$5.87
    """
    print (bcolors.ENDC + "The payment for sell 10 shares: " + bcolors.GREEN + str ( market.payment_for_sell_yes(50,10,10) ))
    
    print (bcolors.ENDC + "Yes (Price: " + str(market.price_yes(50,10)) + ") No (Price: " + str(market.price_no(50,10)) + ")")


if __name__=="__main__":
    main()
