#%%
import pandas as pd
import matplotlib.pyplot as plt
import random 
import numpy as np
#%% Section 1: we define a function that simulates a game. 
# The function only has one variable Edge. 
# Edge variable is set up in a way that to increase the chance of winning, decrease Edge value.
def Game(Edge):
    roll = random.randint(1,100)
    if roll <= Edge: return False # between 1-50 loss
    elif roll> Edge: return True # between 51-99 win
         
#%% Section 2: We define 3 different strategies
# one with (1) no strategy (2) Martingale strategy (3) Fluid Strategy
def No_Strategy(fund, initial_gambler, gambler_count, Edge, C):
    No_Strategy_bust = 0
    No_Strategy_profit =  0
    value = fund
    gambler = initial_gambler
    
    wX, vY = [], []
    
    currentgambler = 1
    while currentgambler <= gambler_count:
        if Game(Edge):
            value += gambler
        else:
            value -= gambler
        wX.append(currentgambler)
        vY.append(value)
        currentgambler += 1
        
    if value <= 0: No_Strategy_bust +=1
 
    plt.plot(wX,vY,C)
    if value > fund: No_Strategy_profit +=1
    return value, No_Strategy_bust


def Martingale_Strategy(fund, initial_gambler, gambler_count, Edge,C):
    value = fund
    gambler = initial_gambler
    doubler_profit = 0
    doubler_busts =0
    
    wX, vY = [], []
    
    currentgambler = 1
    prevgambler = 'win'
    prevAmount = initial_gambler
    
    while currentgambler <= gambler_count:
        if prevgambler =='win':
            if Game(Edge):
                value += gambler
                wX.append(currentgambler)
                vY.append(value)
            else:
                value -= gambler 
                prevgambler = 'loss'
                prevAmount = gambler
                wX.append(currentgambler)
                vY.append(value)   
                if value <= 0: 
                    doubler_busts +=1
                    break
                
        elif prevgambler =='loss':    
            if Game(Edge):
                gambler = prevAmount *2
                if (value - gambler) <0: # not allowing the negative sum to occur
                    gambler = value
                
                value += gambler
                gambler = initial_gambler
                prevgambler ='win'
                wX.append(currentgambler)
                vY.append(value)
            else:
                gambler = prevAmount *2
                if (value - gambler) <0: # not allowing the negative sum to occur
                    gambler = value
                value -= gambler
                prevgambler = 'loss'
                prevAmount = gambler
                wX.append(currentgambler)
                vY.append(value)
                if value <= 0: 
                    doubler_busts +=1
                    break

        currentgambler += 1
    plt.plot(wX, vY,C)
    if value>fund: doubler_profit +=1
    return value, doubler_busts
        
        
def PP_Strategy(Nn,dNn, fund, initial_gambler, gambler_count, Edge, C,alpha, beta, gamma, delta, dt, x0, y0):
    multiple_bust = 0
    multiple_profit = 0
    value = fund
    gambler= initial_gambler
    wX, vY = [], []
    currentgambler =1
    prevgambler = 'win'
 
    prevAmount = initial_gambler
 #### Calculating the random_multuple from the PP model
 # where we randomly choose the number of iteration for the PP model.
    N = random.randrange(Nn,(10*Nn)+1, dNn)
    t= np.arange(N)*dt
    Market, Strat = PP_Multiplier(alpha, beta, gamma, delta, dt, N, t, x0, y0)   
    
    
    if Game==True and Strat[-2]<Strat[-1]: random_multiple = Strat[-1]
    elif Game==False and Strat[-2]>Strat[-1]: random_multiple = Strat[-1]
    else: random_multiple = 1
 ### End of cal     
    while currentgambler <= gambler_count:
        if prevgambler =='win':
            if Game(Edge):
                value += gambler 
                wX.append(currentgambler)
                vY.append(value)
            else:
                value -= gambler 
                prevgambler = 'loss'
                prevAmount = gambler
                wX.append(currentgambler)
                vY.append(value)   
                if value <= 0: 
                    multiple_bust +=1
                    break
                
        elif prevgambler =='loss':
        
            if Game(Edge):
                gambler = prevAmount * random_multiple
                if (value - gambler) <0: # not allowing the negative sum to occur
                    gambler = value
                
                value += gambler
                gambler = initial_gambler
                prevgambler ='win'
                wX.append(currentgambler)
                vY.append(value)
            else:
                gambler = prevAmount * random_multiple
                if (value - gambler) <0: # not allowing the negative sum to occur
                    gambler = value
                value -= gambler
                prevgambler = 'loss'
                prevAmount = gambler
                wX.append(currentgambler)
                vY.append(value)
                if value <= 0: 
                    multiple_bust +=1
                    break

        currentgambler+= 1
    plt.plot(wX, vY,C)
    if value>fund:  
        multiple_profit += 1  
    return value, multiple_bust
#%% 
# Dynamics of The Model
def PP_Multiplier(alpha, beta, gamma, delta, dt, N, t, x0, y0):
    def f(x, y):
        xdot = alpha*x - beta*x*y
        ydot = delta*x*y - gamma*y
        return xdot, ydot
    # State Transition using Runge-Kutta Method
    def next(x, y):
        xdot1, ydot1 = f(x, y)
        xdot2, ydot2 = f(x + xdot1*dt/2, y + ydot1*dt/2)
        xdot3, ydot3 = f(x + xdot2*dt/2, y + ydot2*dt/2)
        xdot4, ydot4 = f(x + xdot3*dt, y + ydot3*dt)
        xnew = x + (xdot1 + 2*xdot2 + 2*xdot3 + xdot4)*dt/6
        ynew = y + (ydot1 + 2*ydot2 + 2*ydot3 + ydot4)*dt/6
        return xnew, ynew
    # Simulation Loop
    x, y = np.zeros(N), np.zeros(N)
    x[0], y[0] = x0, y0
    for k in range(N-1):
        x[k+1], y[k+1] = next(x[k], y[k])
        
    return x, y

def PP_Visualisation(alpha, beta, gamma, delta, dt, N, t, x0, y0):
    x, y= PP_Multiplier(alpha, beta, gamma, delta, dt, N, t, x0, y0)
    plt.subplot(1,2,1)
    plt.plot(t,x, label='Market', linewidth=1)
    plt.plot(t,y, label='Gambler', linewidth=1)
    plt.grid()
    plt.legend(loc = 'upper right')
    plt.xlabel('Time')
    
    plt.subplot(1,2,2)
    plt.plot(x,y, linewidth=1)
    plt.grid()
    plt.xlabel('Market')
    plt.ylabel('Gambler')
    plt.title('Phase Portrait')









