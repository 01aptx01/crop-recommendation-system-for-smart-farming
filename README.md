# Crop Recommendation System for Smart Farming

## Introduction
The Crop Recommendation System for Smart Farming is an intelligent machine learning application designed to help farmers make data-driven decisions. By analyzing critical environmental and soil metrics, the system recommends the best crops to plant and estimates the potential yield and financial profit, optimizing agricultural output and sustainability.

## Features
- **Crop Classification:** Predicts the top 3 most suitable crops based on soil and weather conditions.
- **Yield Prediction:** Estimates the expected harvest volume (in tons/kg) based on area size and environment.
- **Profit Prediction:** Forecasts potential financial returns.
- **Fast & Scalable API:** Provides a robust REST API using FastAPI for seamless frontend or mobile integration.
- **Production Ready:** Fully containerized using Docker for easy deployment across diverse cloud environments.

## Tech Stack
- **Language:** Python 3.10+
- **Machine Learning:** scikit-learn, XGBoost, PyTorch/TensorFlow (Optional)
- **Data Manipulation:** pandas, numpy
- **API Framework:** FastAPI, Uvicorn
- **Containerization:** Docker

## Project Structure
```text
.
├── api/
│   ├── main.py              # FastAPI application and endpoints
│   ├── schemas.py           # Pydantic models for input/output validation
│   └── inference.py         # Helper functions for model loading and prediction
├── data/
│   ├── raw/                 # Original Kaggle dataset
│   └── processed/           # Data with simulated features and targets
├── models/
│   ├── crop_classifier.pkl  # Serialized classification model
│   ├── yield_regressor.pkl  # Serialized yield regression model
│   ├── profit_regressor.pkl # Serialized profit regression model
│   └── scaler.pkl           # Data scaler artifact
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_model_tuning.ipynb
├── src/
│   ├── data/
│   │   ├── simulate_features.py
│   │   ├── simulate_targets.py
│   └── preprocess.py
│   └── models/
│       ├── train_classifier.py
│       └── train_yield_reg.py
├── Dockerfile               # Instructions to build the Docker image
└── requirements.txt         # Project Python dependencies
```

## API Input/Output Specifications

### **Endpoint:** `POST /predict`

**Input (JSON):**
```json
{
  "area_size": 5.5,
  "soil_type": "Loamy",
  "ph": 6.5,
  "nitrogen": 90.0,
  "phosphorus": 42.0,
  "potassium": 43.0,
  "humidity": 82.0,
  "temperature": 20.8,
  "rainfall": 202.9
}
```

**Output (JSON):**
```json
{
  "top_3_crops": [
    {"crop": "Rice", "probability": 0.85},
    {"crop": "Jute", "probability": 0.10},
    {"crop": "Cotton", "probability": 0.04}
  ],
  "predicted_yield": 2450.5,
  "predicted_profit": 12500.00
}
```

## How to Install and Run

### 1. Local Setup
1. Clone the repository and navigate to the project root.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the API server:
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Access the interactive API docs at: `http://localhost:8000/docs`

### 2. Docker Setup
1. Ensure Docker is installed and running on your machine.
2. Build the Docker image:
   ```bash
   docker build -t crop-recommendation-api .
   ```
3. Run the container:
   ```bash
   docker run -d -p 8000:8000 --name crop_api crop-recommendation-api
   ```
4. Access the API at: `http://localhost:8000`