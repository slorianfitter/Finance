import numpy as np
import pandas as pd
from  qpsolvers import solve_qp
from math import sqrt

def opt_portfolio(
    data: pd.DataFrame,
    zielrendite: float = 0.025,
    is_returns: bool = False
) -> dict:
     
    '''
    Die Portfolioauswahl wird durch diese Funktion erleichtert. Zunächst wird das Portfolio mit eingegebener 
    Zielrendite für gleich Periodige Renditen mit einer Leerverkaufsbeschränkung optimiert. 
    Wenn ein Portfolio nicht möglich ist, wird die Beschränkungaufgehoben. 

    - Es können sowohl renditen als auch Preise benutzt werden. 

    - Gibt ein Tuple aus Gewichte (pd.Series) und sigma zurück 

    Ein Error wird ausgegeben wenn die Zielrendite so nicht machbar ist. 
    '''

    if data.shape[1] == 1 and is_returns == False:
        raise ValueError("Kann kein Portfolio aus nur einer Aktie erstellen")

    if data.shape[1] == 1 and is_returns == True:
        raise ValueError("Kann keine Optimierung mit einer einzelnen Spalte voller Renditen vornehmen. " \
        "Bitte mehr als eine Spalte in den Dataframe aufnehmen und darauf achten, dass es mehr als nur einen Eintrag gibt für sinnvolle Ergebnisse")

    # Preise -> Renditen
    if is_returns == False:
        returns = np.log(data).diff().dropna()
    else:
        returns = data.dropna()

    # Erwartungswerte & Kovarianz
    mu = returns.mean().to_numpy()
    cov = returns.cov().to_numpy()  
    n = mu.shape[0]

    # QP-Setup
    P = 2 * cov
    q = np.zeros(n)
    A = np.vstack([np.ones(n), mu]).astype(float)
    b = np.array([1.0, zielrendite])
    G = -np.eye(n)
    h = np.zeros(n)
    weights = solve_qp(P, q, G, h, A, b, solver="quadprog") 


    # Aufhebung der Leerverkaufsbeschränkung
    if weights is None:

        G, h = None, None
    
        weights = solve_qp(P, q, G, h, A, b, solver="quadprog")
    
    if weights is None:
        raise RuntimeError("Optimierungsproblem konnte nicht gelöst werden: Zielrendite evtl. nicht erreichbar")

    sigma = sqrt(weights.T @ cov @ weights)

    
    weights = np.array(weights).flatten()
    weights_df = pd.DataFrame([weights], columns=returns.columns)
    return {
        "weights": weights_df.to_dict(orient="records"),
        "sigma": round(sigma, 10)
    }





