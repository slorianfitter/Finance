# Portfolio-Optimierungsprojekt

## Über das Projekt
Dieses Projekt ist ursprünglich während meiner Klausurvorbereitung für **Finanz- und Versicherungsökonomik** entstanden.  
  
Die Idee: Mit **FastAPI** lassen sich nicht nur Daten, sondern auch Modelle für Prognosen und Simulationen bereitstellen.  
So können Kunden direkt selbst Modelle nutzen, ohne viel Rücksprache, und bekommen die gleichen Ergebnisse wie ich.  

---

## Implementierte Modelle

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

## Update 28.11.2025

Damals habe ich das Projekt nur als Klausurvorbereitung gestartet und möchte nun aber an dem Projekt weiterarbeiten für ein schönes Forecasting. Erstmal möchte ich allerdings noch ein **Faktorenmodell** implementieren.  

Dann muss ich noch einige Paper lesen, um meinen Wissensstand zu aktualisieren und raus aus den Vorlesungen und rein in die Praxis gelangen, um ein möglichst effizientes Modell zu schreiben, welches im Optimalfall die Zukunft vorhersagen kann und dann passend mit täglichem Input ein Portfolio anpassen kann.
