# 🚢 Titanic Survival Predictor

> **TR:** Yapay sinir ağı tabanlı Titanic hayatta kalma tahmin uygulaması.  
> **EN:** A neural network–powered web app that predicts Titanic passenger survival.

---

## 📋 İçindekiler / Table of Contents

- [Türkçe Açıklama](#-türkçe-açıklama)
- [English Description](#-english-description)
- [Kurulum / Installation](#-kurulum--installation)
- [Kullanım / Usage](#-kullanım--usage)
- [Proje Yapısı / Project Structure](#-proje-yapısı--project-structure)
- [Model Detayları / Model Details](#-model-detayları--model-details)
- [Teknolojiler / Technologies](#-teknolojiler--technologies)

---

## 🇹🇷 Türkçe Açıklama

Bu proje, Titanic veri seti üzerinde eğitilmiş bir **Yapay Sinir Ağı (ANN)** kullanarak bir yolcunun hayatta kalıp kalmayacağını tahmin eden interaktif bir web uygulamasıdır.

### Özellikler

- 🧠 **PyTorch** ile sıfırdan oluşturulmuş özel ANN mimarisi (Dropout regularization dahil)
- ⚡ **FastAPI** tabanlı REST API backend
- 🎨 Modern, animasyonlu web arayüzü (HTML, CSS, JavaScript)
- 📊 Tahmin sonucuyla birlikte gerçek zamanlı olasılık çubuğu
- 🔧 Özellik mühendisliği: cinsiyet, yaş, bilet sınıfı, ücret, aile bilgisi ve biniş limanı

### Nasıl Çalışır?

1. Kullanıcı formu doldurur (yolcu sınıfı, cinsiyet, yaş, bilet ücreti vb.)
2. Form verileri FastAPI backend'e POST isteğiyle gönderilir
3. Model verileri standardize ederek ANN'den geçirir
4. Hayatta kalma olasılığı (%) ve karar web arayüzünde gösterilir

---

## 🇬🇧 English Description

This project is an interactive web application that predicts whether a Titanic passenger would have survived, using a custom **Artificial Neural Network (ANN)** trained on the Titanic dataset.

### Features

- 🧠 Custom ANN architecture built from scratch with **PyTorch** (includes Dropout regularization)
- ⚡ **FastAPI**-powered REST API backend
- 🎨 Modern, animated web UI (HTML, CSS, JavaScript)
- 📊 Real-time probability bar displayed alongside prediction result
- 🔧 Feature engineering: gender, age, ticket class, fare, family info, and embarkation port

### How It Works

1. User fills in the form (passenger class, gender, age, ticket fare, etc.)
2. Form data is sent to the FastAPI backend via a POST request
3. The model standardizes the input and passes it through the ANN
4. Survival probability (%) and the final decision are displayed on the web UI

---

## ⚙️ Kurulum / Installation

### Gereksinimler / Requirements

- Python 3.9+
- pip

### Adımlar / Steps

```bash
# 1. Repoyu klonlayın / Clone the repository
git clone https://github.com/YOUR_USERNAME/titanic-survival-predictor.git
cd titanic-survival-predictor

# 2. Sanal ortam oluşturun / Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Bağımlılıkları yükleyin / Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Kullanım / Usage

### 1. Modeli Eğit / Train the Model

Önce modeli eğitmeniz gerekir. / First, you need to train the model.

```bash
python train_model.py
```

Başarılı çıktı şuna benzer olacak: / Successful output will look like:

```
[*] train.csv yukleniyor...
    891 satir bulundu.

[*] Egitim basliyor...

Epoch   0 | Train Loss: 0.6931  Train Acc: 60.0% | Test Loss: 0.6918  Test Acc: 61.2%
Epoch  50 | Train Loss: 0.4821  Train Acc: 78.5% | Test Loss: 0.4903  Test Acc: 77.1%
...
[OK] Egitim tamamlandi! Son Test Accuracy: ~82%
[OK] Model kaydedildi --> models/titanic_model.pth
```

### 2. API Sunucusunu Başlat / Start the API Server

```bash
uvicorn main:app --reload
```

### 3. Tarayıcıda Aç / Open in Browser

```
http://127.0.0.1:8000
```

Formu doldurup **"Tahmini Hesapla"** butonuna basın! / Fill the form and click **"Tahmini Hesapla"**!

---

## 📁 Proje Yapısı / Project Structure

```
titanic-survival-predictor/
│
├── train_model.py        # TR: Model eğitim scripti          / EN: Model training script
├── main.py               # TR: FastAPI backend                / EN: FastAPI backend
├── requirements.txt      # TR: Python bağımlılıkları          / EN: Python dependencies
│
├── train.csv             # TR: Eğitim veri seti (Kaggle)     / EN: Training dataset (Kaggle)
├── test.csv              # TR: Test veri seti                 / EN: Test dataset
├── gender_submission.csv # TR: Örnek tahmin çıktısı          / EN: Sample submission file
│
├── models/
│   └── titanic_model.pth # TR: Eğitilmiş model ağırlıkları  / EN: Trained model weights
│
├── static/
│   ├── index.html        # TR: Web arayüzü                   / EN: Web UI
│   ├── style.css         # TR: Stil dosyası                  / EN: Stylesheet
│   └── script.js         # TR: Ön yüz mantığı                / EN: Frontend logic
│
└── Titanic.ipynb         # TR: Keşifsel veri analizi         / EN: Exploratory data analysis
```

---

## 🧠 Model Detayları / Model Details

| Özellik / Property | Değer / Value |
|---|---|
| Mimari / Architecture | Fully Connected ANN |
| Giriş özellikleri / Input Features | 7 (Pclass, Sex, Age, SibSp, Parch, Fare, Embarked) |
| Katmanlar / Layers | Linear(7→64) → Dropout(0.3) → Linear(64→32) → Dropout(0.2) → Linear(32→1) |
| Aktivasyon / Activation | ReLU (hidden), Sigmoid (output) |
| Kayıp fonksiyonu / Loss Function | Binary Cross Entropy (BCELoss) |
| Optimizasyon / Optimizer | Adam (lr=0.001) |
| Epoch sayısı / Epochs | 300 |
| Test doğruluğu / Test Accuracy | ~82% |
| Regularization | Dropout (0.3, 0.2) |

### Özellik Mühendisliği / Feature Engineering

| Özellik / Feature | İşlem / Processing |
|---|---|
| Age | Median imputation (Pclass & Sex gruplarına göre) |
| Sex | Label encoding: male→0, female→1 |
| Embarked | Label encoding: S→0, C→1, Q→2 |
| Fare | Median imputation |
| Pclass, SibSp, Parch | Olduğu gibi / As-is |
| Tüm özellikler / All features | StandardScaler normalization |

---

## 🛠️ Teknolojiler / Technologies

| Katman / Layer | Teknoloji / Technology |
|---|---|
| **Deep Learning** | PyTorch |
| **Web Framework** | FastAPI |
| **ASGI Server** | Uvicorn |
| **Data Processing** | Pandas, NumPy |
| **Preprocessing** | scikit-learn (StandardScaler) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Font** | Google Fonts — Inter |

---

## 📊 API Referansı / API Reference

### `POST /predict`

Yolcu bilgilerini alıp hayatta kalma olasılığını döndürür.  
Takes passenger data and returns survival probability.

**Request Body:**

```json
{
  "pclass":   1,
  "sex":      1,
  "age":      29.0,
  "sibsp":    0,
  "parch":    0,
  "fare":     211.34,
  "embarked": 1
}
```

**Response:**

```json
{
  "survived":    true,
  "probability": 92.4
}
```

---

## 📄 Lisans / License

Bu proje MIT Lisansı ile lisanslanmıştır. / This project is licensed under the MIT License.

---

## 🙏 Kaynaklar / Credits

- Veri seti / Dataset: [Kaggle — Titanic: Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic)
- Model framework: [PyTorch](https://pytorch.org/)
- API framework: [FastAPI](https://fastapi.tiangolo.com/)
