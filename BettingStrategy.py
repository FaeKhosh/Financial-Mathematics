#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: faekhoshsepehr
"""

#%% 
from UtilZ import *
import matplotlib.pyplot as plt
#%%
plt.close('all') 

sampleSize = 10000
startFund = 10000
wagerSize = 100
wagerCount = 100
# Since the bet size is linked to starting fund its better to set it as % of bet size.
# for example bet-size/startfund = 100/10000
N,dNn = 100, 10
alpha, beta, gamma, delta = 1.1, 0.4, 0.4, 0.1
dt, x0 = 0.01, 30
y0 = 0.2*x0
#%% Models
y= 0    
Number_Bust_NS, Number_Bust_MS = 0,0
while y < sampleSize:
    V1, No_Strategy_bust = No_Strategy(startFund, wagerSize,wagerCount, 50,'r') 
    Number_Bust_NS += No_Strategy_bust
    V2, doubler_busts = Martingale_Strategy(startFund, wagerSize, wagerCount, 50,'g') 
    Number_Bust_MS  += doubler_busts
    y +=1 
plt.title('No Strategy vs Martingle Strategy') 
plt.ylabel('Account value')
plt.xlabel('Gambler Count')
plt.legend(('No-Strategy', 'Martingle Strategy'))
#plt.axhline(0, c='black')

print('% of no-strategy brokes:', Number_Bust_NS/float(y) *100 )
print('% of no-strategy winners:', 100- (Number_Bust_NS/float(y) *100 ))

print('% of martingale brokes:', Number_Bust_MS/float(y) *100 )
print('% of martingale  winners:', 100- (Number_Bust_MS/float(y) *100 ))
#%% second Strat
x= 0 
Number_Bust_NS, Number_Bust_PP = 0,0   
while x < sampleSize:
    V3, No_Strategy_bust = No_Strategy(startFund, wagerSize,wagerCount, 50,'r') 
    Number_Bust_NS += No_Strategy_bust
    V4, PP_Strategy_bust = PP_Strategy(Nn,dNn,startFund, wagerSize, wagerCount, 50,'b',alpha, beta, gamma, delta, dt, x0, y0)  
    Number_Bust_PP +=  PP_Strategy_bust
    x +=1 
    
plt.title('No-Strategy vs PP Strategy') 
plt.ylabel('Account value')
plt.xlabel('Gambler Count')
plt.legend(('No Strategy', 'PP Strategy'))
#plt.axhline(0, c='black')
print('% of no-strategy brokes:', Number_Bust_NS/float(y) *100 )
print('% of no-strategy winners:', 100- (Number_Bust_NS/float(y) *100 ))

print('% of PP brokes:', Number_Bust_PP/float(y) *100 )
print('% of PP  winners:', 100- (Number_Bust_PP/float(y) *100 ))
# %%PP Strategy
PP_Visualisation(alpha, beta, gamma, delta, dt, N, t, x0, y0)
### End