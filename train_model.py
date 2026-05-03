"""
Titanic Survival Predictor - Model Eğitim Scripti
Kullanım: python train_model.py
"""
import os
import pandas as pd
import numpy as np
import torch
from torch import nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

os.makedirs("models", exist_ok=True)

# ── Veri Yükleme ──────────────────────────────────────────────────────────────
print("[*] train.csv yukleniyor...")
df = pd.read_csv("train.csv")
print(f"    {len(df)} satir bulundu.")

# ── Temizleme ─────────────────────────────────────────────────────────────────
df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"], inplace=True)

df["Age"] = df.groupby(["Pclass", "Sex"])["Age"].transform(
    lambda x: x.fillna(x.median())
)
df["Fare"] = df["Fare"].fillna(df["Fare"].median())

df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# ── Özellik / Hedef ───────────────────────────────────────────────────────────
X = df.drop(columns=["Survived"])
y = df["Survived"]

# ── Önce Split, Sonra Scale ───────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

X_train_t = torch.tensor(X_train_scaled, dtype=torch.float32)
X_test_t  = torch.tensor(X_test_scaled,  dtype=torch.float32)
y_train_t = torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)
y_test_t  = torch.tensor(y_test.values,  dtype=torch.float32).unsqueeze(1)

# ── Model Tanımı ──────────────────────────────────────────────────────────────
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


model     = TitanicClassifier()
loss_fn   = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


def calc_acc(y_true, y_pred):
    correct = torch.eq(y_true.squeeze(), y_pred.squeeze()).sum().item()
    return correct / len(y_true) * 100


# ── Eğitim ────────────────────────────────────────────────────────────────────
print("\n[*] Egitim basliyor...\n")
EPOCHS = 300

for epoch in range(EPOCHS):
    model.train()
    logits = model(X_train_t).squeeze()
    loss   = loss_fn(logits, y_train_t.squeeze())
    preds  = torch.round(logits)
    acc    = calc_acc(y_train_t, preds)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    model.eval()
    with torch.inference_mode():
        t_logits = model(X_test_t).squeeze()
        t_loss   = loss_fn(t_logits, y_test_t.squeeze())
        t_preds  = torch.round(t_logits)
        t_acc    = calc_acc(y_test_t, t_preds)

    if epoch % 50 == 0:
        print(
            f"Epoch {epoch:3d} | "
            f"Train Loss: {loss:.4f}  Train Acc: {acc:.1f}% | "
            f"Test Loss: {t_loss:.4f}  Test Acc: {t_acc:.1f}%"
        )

print(f"\n[OK] Egitim tamamlandi! Son Test Accuracy: {t_acc:.1f}%")

# ── Kaydet ────────────────────────────────────────────────────────────────────
torch.save(
    {
        "model_state_dict": model.state_dict(),
        "scaler_mean":  scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "feature_names": list(X.columns),
    },
    "models/titanic_model.pth",
)
print("[OK] Model kaydedildi --> models/titanic_model.pth")
