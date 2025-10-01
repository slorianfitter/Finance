import pandas as pd
import numpy as np
from math import sqrt


def portfolio_entwicklung(portfoliokurse:pd.DataFrame, 
                          Haltedauer: float = 2.0,
                          Handelstage:int = 252) -> pd.DataFrame:
    

    portfoliokurse.index.name = None
    # Matrixform (Anzahl der Zeilen, Anzahl der Spalten) -> Mathematisch, nicht Numpy shapes

    portfoliokurse_ints = portfoliokurse.select_dtypes(include=[np.number])


    numpy_kurse = portfoliokurse_ints.to_numpy() #(T,n)

    S0 = numpy_kurse[-1] #(1,n)


    log_returns = np.log(numpy_kurse[1:]) - np.log(numpy_kurse[:-1]) #(T-1,n)
    
    mu_daily = np.nanmean(log_returns, axis = 0) #(1,n)

    mu_annual = mu_daily * Handelstage #(1,n)

    sigma_daily = np.nanstd(log_returns, axis = 0) #(1,n)

    sigma_annual = sigma_daily * sqrt(Handelstage) #(1,n)


    # Zeithandling und Wiender Prozess
    n_steps = int(Haltedauer*Handelstage)
    dt = Haltedauer/n_steps #(1,1)
    

    Z = np.random.randn(n_steps, S0.size) # (T,n)
    W = np.cumsum(np.sqrt(dt) * Z, axis=0)  #(T,n)
    t = np.linspace(0, Haltedauer, n_steps)[:,None] # (n_steps,1)



    drift = (mu_annual - 0.5 * sigma_annual**2) * t
    diff  = sigma_annual * W
    S = S0 * np.exp(drift + diff)    

    # 5) Als DataFrame zurück mit Originalspalten
    return pd.DataFrame(S, columns=portfoliokurse_ints.columns).reset_index(drop=True)



