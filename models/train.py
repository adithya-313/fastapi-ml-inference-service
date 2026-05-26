# =============================================================================
# IMPORTS
# =============================================================================
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

# =============================================================================
# TRAINING DATA
# =============================================================================
# We want the model to learn:  y = (feature1 * 2.0) + (feature2 * 3.0)
# Use non-collinear feature values so sklearn recovers exact [2.0, 3.0] coefs.
X = np.array([[0, 0], [1, 0], [0, 1], [2, 1], [1, 2], [3, 4]])
y = np.array([0.0, 2.0, 3.0, 7.0, 8.0, 18.0])  # 2*x1 + 3*x2

# =============================================================================
# MODEL TRAINING
# =============================================================================
model = LinearRegression()
model.fit(X, y)

# =============================================================================
# SAVE MODEL
# =============================================================================
joblib.dump(model, 'models/model.joblib')
print("Model saved to models/model.joblib")
print(f"Coefficients: {model.coef_}, Intercept: {model.intercept_}")
print(f"Test [10, 20] -> {model.predict(np.array([[10.0, 20.0]]))[0]}")
