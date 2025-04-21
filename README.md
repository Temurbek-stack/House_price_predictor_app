# 🏠 House Price Prediction Platform

An interactive, ML-powered web platform that allows users to **predict the market price of residential real estate in Uzbekistan** based on property characteristics, location, and nearby infrastructure. It uses **machine learning models trained on real market data** to offer fast, affordable, and transparent price evaluations.

---
## 🌐 Live Demo

🔗 [Try the live app here](https://house-price-predictor-app.onrender.com/)
---


## 🚀 Key Features

- 🧠 **ML-powered prediction**: Uses trained machine learning models to estimate housing prices.  
- 🏙️ **Detailed property input form**: Input location, layout, condition, amenities, and more.  
- 📄 **Downloadable PDF report**: Generate and download a full valuation report.  
- 📊 **User feedback integration**: Built-in feedback mechanism for continuous improvement.  
- 📌 **Bilingual interface**: Combines Uzbek and English text to reach a broader user base.  

---

## 📦 Tech Stack

- `Python`  
- `Dash` + `Plotly` + `Dash Bootstrap Components`  
- `pandas` for data processing  
- `joblib` for loading trained models  
- `FPDF` for report generation  

---

## 🤖 Machine Learning Stack

- `LightGBM` – core prediction model  
- `scikit-learn` – for preprocessing and model integration  
- `Optuna` – hyperparameter tuning using Bayesian Optimization  
- `NumPy`, `pandas` – for data handling and feature engineering  
- `joblib` – model persistence and loading  

---

## 🧪 Model Details

The platform uses **LightGBM**, a high-performance gradient boosting framework, known for:

- ⚡ **Fast training and prediction speed**  
- 🧠 **High accuracy with large datasets**  
- 🌳 **Efficient handling of categorical features**  
- 🚫 **Built-in regularization to prevent overfitting**  

Prediction is based on:

- 📐 Area, number of rooms, floor level  
- 🏢 Building type, apartment layout, construction year, ownership type  
- 🔧 Renovation level and amenities (e.g., school, hospital, cafes nearby)  
- 🌍 Location-specific features and surrounding infrastructure  

> 📓 **Note**: A snippet from modeling pipeline, including training, validation, and hyperparameter tuning, is available in the Jupyter notebook located in the [`model`](./model) folder.
---

## 🧹 Data Collection & Cleaning

- **Data Collection**:  
  Data is collected through **web scraping** from the most popular real estate platforms in Uzbekistan. Thousands of listings are scraped regularly to ensure the model reflects current market trends.

  - 🔒 Privacy Notice: For privacy and compliance reasons, the raw data collected and the dataset used for training cannot be shared in this repository.

- **Data Cleaning**:  
  - 📍 **Micro-level location identification**: Neighborhoods (mahallas) are extracted from ad descriptions using NLP techniques to ensure geographic precision.  
  - 🧼 **Standardization of features**: Property attributes such as floor level, area, layout, and price are standardized across listings with inconsistent formats.  
  - 📊 **Outlier removal**: Extreme values (e.g., unrealistically high or low prices, or very large areas) are filtered using statistical thresholds.  
  - 🧠 **Missing value imputation**: Smart imputation methods (e.g., using medians, k-NN, or regression models) are applied to fill gaps in critical variables.  
  - 💬 **Text parsing**: Description fields are mined for additional features like proximity to transport, schools, or newly renovated status.

---
