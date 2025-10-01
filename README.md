# Portfolio-Optimierungsprojekt

## Über das Projekt
Dieses Projekt ist ursprünglich während meiner Klausurvorbereitung für **Finanz- und Versicherungsökonomik** entstanden.  
Da an der HHU hauptsächlich mit *R* im Studiengang VWL gearbeitet wird, habe ich mich entschieden, ein eigenes Projekt in **Python** umzusetzen.  

Die Idee: Mit **FastAPI** lassen sich nicht nur Daten, sondern auch Modelle für Prognosen und Simulationen bereitstellen.  
So können Kunden direkt selbst Modelle nutzen, ohne viel Rücksprache, und bekommen die gleichen Ergebnisse wie ich.  

---

## Implementierte Modelle

> ⚠️ Hinweis:  
> Die folgenden Modelle sind didaktisch gedacht und spiegeln die Realität nur sehr vereinfacht wider.  
> In der Praxis werden sie in dieser Form von professionellen Anlegern nicht mehr verwendet.

1. **Portfolioselektion nach Markowitz**  
   - Endpoint: `POST /prediction/portfolioselection`  
   - Input (JSON):  
     ```json
     {
       "header": ["StockA", "StockB"],
       "data": [[0.05, 0.02], [0.03, 0.01], [0.04, 0.03]],
       "zielrendite": 0.02,
       "is_returns": true
     }
     ```
   - Output:  
     ```json
     {
       "weights": [{"StockA": 0.0, "StockB": 1.0}],
       "sigma": 0.01
     }
     ```

2. **Capital Asset Pricing Model (CAPM)**  
   - Endpoint: `POST /prediction/capm`  
   - Input:  
     ```json
     {
       "header": ["StockA", "StockB"],
       "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
       "data": [[0.05, 0.02], [0.03, 0.01], [0.04, 0.03]],
       "is_returns": true
     }
     ```
   - Output:  
     ```json
     {
       "result": {"StockA": -1.74, "StockB": -4.29}
     }
     ```

3. **Brownsche Bewegungen**  
   - Endpoint: `POST /prediction/brownsche_bewegung`  
   - Input:  
     ```json
     {
       "header": ["StockA", "StockB"],
       "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
       "data": [[100, 200], [101, 198], [102, 201]],
       "handelstage": 252,
       "haltedauer": 2.0
     }
     ```
   - Output (gekürzt):  
     ```json
     {
       "result": [
         {"StockA": 100.0, "StockB": 200.0},
         {"StockA": 101.5, "StockB": 198.3},
         {"StockA": 102.7, "StockB": 201.1}
       ]
     }
     ```

---

## Fazit & Ausblick
- Gelungenes Projekt zur Verbindung von **Finanzmathematik** und **APIs**.  
- Erstes Gefühl für eine richtige **Pipeline**.  
- Frontend ist noch sehr rudimentär – mögliche Erweiterungen:  
  - Visualisierungen der Ergebnisse direkt über die API zurückgeben  
  - Erweiterung um Fama-French 3- oder 5-Faktorenmodell  

---

## Technologien
- **Python 3.12**  
- **FastAPI**  
- **Pydantic** 
- **Uvicorn** 
- **Pandas / NumPy**  
- **Statsmodels**  
- **Math**
- **Qpsolvers**
