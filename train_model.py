import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("dataset.csv")

# Print column names
print("Columns in Dataset:")
print(df.columns)

# ------------------------------
# CHANGE THESE COLUMN NAMES
# ------------------------------
X = df[[
    "Life expectancy",
    "Mean years of schooling",
    "Expected years of schooling",
    "GNI per capita"
]]

y = df["HDI Category"]

# ------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

joblib.dump(model, "hdi_model.pkl")

print("Model Saved Successfully!")