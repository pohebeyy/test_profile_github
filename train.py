import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split

TARGET = "strong_project"


data = pd.read_csv("data/project_scores.csv")
X = data.drop(columns=[TARGET]).values
y = data[TARGET].values

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(f"Сильных проектов в тесте: {y_test.mean() * 100:.0f}%")
print(f"Точность: {precision * 100:.0f}%")
print(f"Полнота:  {recall * 100:.0f}%")

joblib.dump(model, "model.pkl")
