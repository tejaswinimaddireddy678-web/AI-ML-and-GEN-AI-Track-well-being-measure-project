import pandas as pd

# Read dataset
df = pd.read_csv("dataset.csv")

print("===== LIFE EXPECTANCY COLUMNS =====")
for col in df.columns:
    if "life" in col.lower():
        print(col)

print("\n===== SCHOOL COLUMNS =====")
for col in df.columns:
    if "school" in col.lower():
        print(col)

print("\n===== GNI / INCOME COLUMNS =====")
for col in df.columns:
    if "gni" in col.lower() or "income" in col.lower():
        print(col)

print("\n===== HDI COLUMNS =====")
for col in df.columns:
    if "human development" in col.lower() or "hdi" in col.lower():
        print(col)