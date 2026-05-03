"""
Titanic Survival Predictor — FastAPI Backend
Çalıştırma: uvicorn main:app --reload
"""
from pathlib import Path

import numpy as np
import torch
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from torch import nn

# ── Model Tanımı (train_model.py ile aynı) ────────────────────────────────────
class TitanicClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = nn.Sequential(
            nn.Linear(7, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.layer(x)


# ── Model Yükleme ─────────────────────────────────────────────────────────────
MODEL_PATH = Path("models/titanic_model.pth")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "❌  models/titanic_model.pth bulunamadı!\n"
        "Önce  python train_model.py  komutunu çalıştırın."
    )

checkpoint   = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
model        = TitanicClassifier()
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

scaler_mean  = np.array(checkpoint["scaler_mean"],  dtype=np.float64)
scaler_scale = np.array(checkpoint["scaler_scale"], dtype=np.float64)

# ── FastAPI ───────────────────────────────────────────────────────────────────
app = FastAPI(title="Titanic Survival Predictor")
app.mount("/static", StaticFiles(directory="static"), name="static")


class PassengerData(BaseModel):
    pclass:   int    # 1, 2, 3
    sex:      int    # 0 = erkek  1 = kadın
    age:      float
    sibsp:    int
    parch:    int
    fare:     float
    embarked: int    # 0 = S  1 = C  2 = Q


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/predict")
async def predict(data: PassengerData):
    # Sıra: Pclass, Sex, Age, SibSp, Parch, Fare, Embarked
    features = np.array(
        [[data.pclass, data.sex, data.age,
          data.sibsp, data.parch, data.fare, data.embarked]],
        dtype=np.float64,
    )
    features_scaled = (features - scaler_mean) / scaler_scale
    tensor = torch.tensor(features_scaled, dtype=torch.float32)

    with torch.inference_mode():
        prob = float(model(tensor).item())

    return {
        "survived":    prob >= 0.5,
        "probability": round(prob * 100, 1),
    }
