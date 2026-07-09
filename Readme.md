# 📈 Stock Price Prediction

A Flask web app for uploading stock data and visualizing closing price trends using multiple ML models — with a multi-model comparison dashboard.

---

## Features

- Upload stock data as CSV, XLS, or XLSX
- Choose from **6 supervised** / **3 unsupervised** ML models via a custom styled dropdown
- View Actual vs Predicted chart with a data summary panel
- Multi-Model Comparison Dashboard — runs all 6 supervised models at once, shows forecast overlay and accuracy metrics (R², MAE, RMSE)
- Light / Dark theme toggle that persists across pages (respects OS preference on first visit)
- Auto-opens browser on `python app.py`

---

## ML Models

### Supervised (Forecast)

| Model | Notes |
|---|---|
| Linear Regression | Fast baseline, straight-line trend |
| Multiple Regression | Uses date index with moving-average features (MA20, MA50) when available |
| Polynomial Regression | Captures curved, non-linear trend lines |
| KNN Regressor | Local-neighborhood based regression |
| Random Forest Regressor | Ensemble model, robust to non-linear patterns |
| Decision Tree Regressor | Interpretable tree-based model (max depth 5) |

### Unsupervised (Analysis)

| Model | Notes |
|---|---|
| K-Means Clustering | Groups data points into 3 behavioural clusters |
| Isolation Forest | Detects anomalies and outliers in price data |
| One-Class SVM | Novelty detection — learns the boundary of normal data (RBF kernel, nu=0.05) |

---

## Input Format

The application supports **generic sequential data**. It will automatically detect:
1. **Date/Time column** (if none is found, it generates a sequence index).
2. **Target column** (looks for "Close", "Target", "y", or defaults to the last numeric column).

Example of a valid file:

| Date | Sales |
|---|---|
| 2024-01-01 | 150.00 |
| 2024-01-02 | 152.50 |

Extra columns are ignored.

---

## Project Structure

```
STOCK-PREDICTION/
├── app.py                  # Flask routes (/, /compare)
├── model.py                # Data prep, ML training, chart generation
├── ml_models/              # Individual model classes
│   ├── linear_regression.py
│   ├── multiple_regression.py
│   ├── logistic_regression.py
│   ├── polynomial_regression.py
│   ├── knn_regressor.py
│   ├── random_forest_regression.py
│   ├── decision_tree_regression.py
│   ├── kmeans_clustering.py
│   ├── isolation_forest.py
│   ├── one_class_svm.py
│   └── utils.py            # Data loading & volatility helpers
├── uploads/                # Uploaded files (auto-created)
├── static/
│   ├── graph.png           # Single-model chart output
│   ├── compare_overlay.png # Multi-model overlay chart
│   ├── compare_accuracy.png# Accuracy bar chart
│   ├── styles_index.css
│   └── styles_result.css
└── templates/
    ├── index.html          # Upload page
    ├── result.html         # Single model result page
    └── compare.html        # Multi-model comparison dashboard
```

---

## Installation

```bash
git clone https://github.com/sujalkarawade/STOCK-PREDICTION.git
cd STOCK-PREDICTION
pip install flask pandas scikit-learn matplotlib openpyxl werkzeug numpy
```

---

## Running

```bash
python app.py
```

Browser opens automatically at `http://127.0.0.1:5000`.

---

## Technologies

| | |
|---|---|
| Python + Flask | Backend and routing |
| Pandas + NumPy | Data loading and preprocessing |
| Scikit-learn | Linear, Multiple, Polynomial, KNN, Random Forest, Decision Tree, K-Means, Isolation Forest, One-Class SVM, metrics |
| Matplotlib | Chart generation |
| HTML / CSS / JS | Frontend UI with theme support |

---

## Author

**Sujal Karawade** — Engineering Student

---

## License

Open-source, free to use for learning and educational purposes.
