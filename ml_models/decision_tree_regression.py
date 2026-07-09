from sklearn.tree import DecisionTreeRegressor


class DecisionTreeRegressionModel:
    def __init__(self, max_depth=5, random_state=42):
        self.model = DecisionTreeRegressor(
            max_depth=max_depth,
            random_state=random_state,
        )

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
