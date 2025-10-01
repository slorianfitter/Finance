import pandas as pd
import numpy as np
import statsmodels.api as sm
import yfinance as yf
import pandas_datareader.data as web


def capm_beta(data:pd.DataFrame, is_returns:bool = False) -> pd.Series:

    '''

    Diese Funktion berechnet das Beta des CAPM. Damit das Beta auch richtig geschätzt werden kann muss folgendes gelten:
    
    - Es muss ein Datum enthallten sein. Hierbei ist es indifferent ob als Index oder als einzelne Spalte. 
      Die Spalte muss aber dann den type "datetime" besitzen und das klassische Format YY-MM-DD besitzen

    Als Output wird eine Serie ausgegeben, mit den Tickern als Index. Wenn das CAPM nicht gilt -> alpha != 0 /  signifikanz
    dann wird eine None für das Beta eingetragen.
    
    Es dürfen auch Renditen direkt benutzt werden, dann aber bitte auf is_returns=True aufpassen.

    '''

    # Start- und Endzeitpunkt für Beta
    if any(data.select_dtypes(include="datetime")):
        
        # Erste Spalte vom Typ datetime suchen
        date_col = data.select_dtypes(include=["datetime"]).columns[0]

        # Diese Spalte als Index setzen -> Tbills und S&P 500 haben gleichen Index
        data = data.set_index(date_col)


    # Start/Ende/Delta berechnen -> für individuelle renditen und betas
    start   = data.index.min()
    end     = data.index.max()
    delta_t = data.index.to_series().diff().dt.days.fillna(1)

    
    # Index (Marktwertgewichtet) und risikofreie Zins holen
    market_data = yf.download("^GSPC", start=start, end=end, auto_adjust = False)["Adj Close"]
    

    # Import des "risikolosen Zinses" -> hier amerikanische Staatsanleihen
    rf = web.DataReader("DTB4WK", "fred", start, end) / 100
    

    # "risikoloser" Zins angepasst an das Zeitintervall 
    price_tbill = 1 - rf["DTB4WK"] * 28 / 360
    gross_28d   = 1 / price_tbill
    rf_period   = gross_28d ** (delta_t / 28) - 1

    rf_period.name = "rf"


    # join damit die Daten passen
    combined = data.join(market_data, how="left").dropna()
    combined = combined.rename(columns={"^GSPC":"mkt"})


    # Marktrenditen
    combined["mkt"] = np.log(combined["mkt"]).diff()


    if not is_returns:
    # Renditen des Inputs
        for col in data.columns:
            combined[col] = np.log(combined[col]).diff()
    
    combined = combined.join(rf_period, how="left").dropna()


    # Capm schätzen 
    betas = []

    ueberrendite_market = combined["mkt"] - combined["rf"]

    for col in combined.columns:
        if col in ["rf", "mkt"]:
            continue

        ueberrendite_data = combined[col] - combined["rf"]

        # beide ohne NaNs
        y = ueberrendite_data.dropna()
        x = pd.DataFrame({"mkt_überrendite": ueberrendite_market.loc[y.index]})
        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()
        beta = model.params["mkt_überrendite"]

        betas.append(beta)

    beta_series = pd.Series(betas, index=data.columns, name="Beta")

    return beta_series




    