# aliyah/predictors.py

import numpy as np
from scipy.stats import norm

class LinearPredictors:
    """
    Implements MALP and LSLP, with CCC, PCC, MSE, confidence and prediction intervals.
    """

    def __init__(self, X, Y):
        """
        Parameters
        ----------
        X : array-like or DataFrame, shape (n_samples, n_features)
            Predictors
        Y : array-like, shape (n_samples,)
            Response variable
        """
        self.X = np.asarray(X)
        self.Y = np.asarray(Y)
        self.n = self.X.shape[0]
        self.p = self.X.shape[1] if self.X.ndim > 1 else 1
        self.mu_X = np.mean(self.X, axis=0)
        self.mu_Y = np.mean(self.Y)
        self.S_X = np.cov(self.X, rowvar=False, ddof=1) if self.p > 1 else np.var(self.X, ddof=1)
        self.S_Y = np.var(self.Y, ddof=1)
        self.S_XY = np.cov(self.Y, self.X, rowvar=False, ddof=1)[0, 1:] if self.p > 1 else np.cov(self.Y, self.X, ddof=1)[0, 1]

        if self.p > 1 and self.S_XY.ndim == 0:
            self.S_XY = np.array([self.S_XY])
        self.inv_S_X = np.linalg.inv(self.S_X) if self.p > 1 else 1.0 / self.S_X
        self.S_YX = self.S_XY if self.p > 1 else np.array([self.S_XY])

    def fit_LSLP(self):
        """Fits the classical Least-Squares Linear Predictor."""
        beta = self.S_YX @ self.inv_S_X if self.p > 1 else self.S_YX * self.inv_S_X
        alpha = self.mu_Y - beta @ self.mu_X if self.p > 1 else self.mu_Y - beta * self.mu_X
        return alpha, beta

    def fit_MALP(self):
        """Fits the EMPIRICAL Maximum Agreement Linear Predictor."""
        gamma2 = (self.S_YX @ self.inv_S_X @ self.S_XY) / self.S_Y if self.p > 1 else (self.S_YX * self.inv_S_X * self.S_XY) / self.S_Y
        gamma = np.sqrt(abs(gamma2))
        beta = (1 / gamma) * (self.S_YX @ self.inv_S_X) if self.p > 1 else (1 / gamma) * self.S_YX * self.inv_S_X
        alpha = self.mu_Y - beta @ self.mu_X if self.p > 1 else self.mu_Y - beta * self.mu_X
        return alpha, beta, gamma

    def predict(self, X_new, method="malp"):
        """Predicts Y for new X using chosen method."""
        X_new = np.asarray(X_new)
        if method.lower() == "malp":
            alpha, beta, _ = self.fit_MALP()
        elif method.lower() == "lslp":
            alpha, beta = self.fit_LSLP()
        else:
            raise ValueError("method must be 'malp' or 'lslp'")
        return alpha + np.dot(X_new, beta)

    @staticmethod
    def ccc(y_true, y_pred):
        """Concordance correlation coefficient."""
        mean_true = np.mean(y_true)
        mean_pred = np.mean(y_pred)
        var_true = np.var(y_true)
        var_pred = np.var(y_pred)
        cov = np.mean((y_true - mean_true) * (y_pred - mean_pred))
        numerator = 2 * cov
        denominator = var_true + var_pred + (mean_true - mean_pred) ** 2
        return