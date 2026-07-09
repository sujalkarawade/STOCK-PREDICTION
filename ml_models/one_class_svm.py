from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler


class OneClassSVMModel:
    def __init__(self, nu=0.05, kernel="rbf", gamma="scale"):
        self.scaler = StandardScaler()
        self.model = OneClassSVM(nu=nu, kernel=kernel, gamma=gamma)

    def fit(self, X):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)  # returns +1 (normal) or -1 (novelty)
