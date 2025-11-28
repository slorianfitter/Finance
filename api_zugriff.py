from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from models import portfolio_selection, capm, brownsche_bewegungen
import pandas as pd

class Portfolioselection_Prediction_Requirements(BaseModel):
    header: list[str]
    data: list[list[float]]
    zielrendite: float
    is_returns: bool = False

class Capm_Prediction_Requirements(BaseModel):
    header: list[str]
    date: list[str]
    data: list[list[float]]
    is_returns: bool = False

class Brownian_Prediction_Requirements(BaseModel):
    header: list[str]
    date: list[str]
    data: list[list[float]]
    handelstage: int = 252
    haltedauer: float = 2.0

api = FastAPI()

@api.get("/")
def list_models():
    return {
        "info": "Diese API verfügt über 3 Modelle. Jedes Modell kann separat aufgerufen werden.",
        "models": [
            {"id": 1, "model": "Portfolioselection nach Markowitz", "endpoint": "http://127.0.0.1:8000/prediction/portfolioselection"},
            {"id": 2, "model": "CAPM", "endpoint": "http://127.0.0.1:8000/prediction/capm"},
            {"id": 3, "model": "Brownsche Bewegungen", "endpoint": "http://127.0.0.1:8000/prediction/brownsche_bewegung"}
        ]
    }

@api.post("/prediction/portfolioselection")
def portfolio_prediction(req: Portfolioselection_Prediction_Requirements):
    df = pd.DataFrame(req.data, columns=req.header)
    result = portfolio_selection.opt_portfolio(df, req.zielrendite, req.is_returns)
    return result

@api.post("/prediction/capm")
def capm_prediction(req: Capm_Prediction_Requirements):
    df = pd.DataFrame(req.data, columns=req.header, index=pd.to_datetime(req.date))

    result = capm.capm_beta(df, req.is_returns)
    return {"result": result.to_dict()}


@api.post("/prediction/brownsche_bewegung")
def brownian_prediction(req: Brownian_Prediction_Requirements):
    df = pd.DataFrame(req.data, columns=req.header, index = pd.to_datetime(req.date))
    result = brownsche_bewegungen.portfolio_entwicklung(df, req.haltedauer, req.handelstage)
    return {"result": result.to_dict(orient="records")}

if __name__ == "__main__":
    uvicorn.run("frontend:api", port=8000, reload=True)
