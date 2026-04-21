# Aliyah

Aliyah is a Python package for predictive modeling using **Maximum Agreement Linear Predictor (MALP)** and **Least Squares Linear Predictor (LSLP)**. It includes agreement metrics like **Concordance Correlation Coefficient (CCC)** and **Pearson Correlation Coefficient (PCC)**, plus confidence intervals and mean squared error (MSE) for model evaluation.

Designed for data scientists, engineers, and consultants who need interpretable, statistically grounded predictions.

---

## 🚀 Features

- ✅ Fit MALP and LSLP models
- 📈 Predict new values with confidence intervals
- 📊 Evaluate model agreement using CCC, PCC, and MSE
- 🧠 Supports multivariate and univariate predictors
- 🔍 Lightweight and dependency-friendly (NumPy + SciPy)

---

## 📦 Installation

```bash
pip install aliyah

Useage
from aliyah_predictor import LinearPredictors

# Sample data
X = [[1, 2], [2, 3], [3, 4]]
y = [2, 3, 5]

# Initialize predictor with MALP method
model = LinearPredictors(method="malp")

# Fit and predict
model.fit(X, y)
predictions = model.predict(X)

# Evaluate agreement
metrics = model.evaluate(y, predictions)
print(metrics)

Expected Output

{
    'CCC': 0.98,
    'PCC': 0.99,
    'MSE': 0.12
}

License
This project is licensed under the MIT License. See the LICENSE file for details.

Author
Created by Kevin Clarke For consulting, integration, or support, visit GitHub or reach out via email.
