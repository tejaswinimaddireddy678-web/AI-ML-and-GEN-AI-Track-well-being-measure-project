import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Load and prepare dataset
CSV_PATH = 'Human Development Index - Full.csv'

def load_data():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Missing file: {CSV_PATH}. Please place it in the same folder as app.py")
    
    df = pd.read_csv(CSV_PATH)
    
    # Strip whitespaces from column names
    df.columns = df.columns.str.strip()
    return df

try:
    df_hdi = load_data()
except Exception as e:
    print(f"Error loading CSV: {e}")
    df_hdi = None

@app.route('/')
def home():
    # Send a list of countries for the dropdown menu
    countries = []
    if df_hdi is not None:
        countries = df_hdi[['ISO3', 'Country']].dropna().to_dict(orient='records')
    return render_template('index.html', countries=countries)

@app.route('/api/country/<iso3>')
def get_country_data(iso3):
    if df_hdi is None:
        return jsonify({"error": "Dataset not loaded"}), 500
    
    # Find matching country row
    country_row = df_hdi[df_hdi['ISO3'] == iso3.upper()]
    if country_row.empty:
        return jsonify({"error": "Country not found"}), 404
    
    row = country_row.iloc[0]
    
    # Extract historical HDI (1990 to 2021)
    years = [str(year) for year in range(1990, 2022)]
    hdi_history = []
    for year in years:
        col = f"Human Development Index ({year})"
        val = row.get(col, None)
        hdi_history.append(float(val) if pd.notna(val) else None)

    # Grab the latest metrics (2021) for simulation baselines
    # Note: If your CSV uses different column naming patterns, adjust these fallback values
    life_exp_2021 = row.get('Life Expectancy at Birth (2021)', 70.0)
    expected_school_2021 = row.get('Expected Years of Schooling (2021)', 12.0)
    mean_school_2021 = row.get('Mean Years of Schooling (2021)', 8.0)
    gni_2021 = row.get('Gross National Income Per Capita (2021)', 10000.0)

    # Convert to standard Python float/strip NaNs
    data = {
        "country": row['Country'],
        "iso3": row['ISO3'],
        "group": row.get('Human Development Groups', 'Unknown'),
        "region": row.get('UNDP Developing Regions', 'N/A'),
        "rank_2021": int(row['HDI Rank (2021)']) if pd.notna(row.get('HDI Rank (2021)')) else "N/A",
        "hdi_2021": float(row['Human Development Index (2021)']) if pd.notna(row.get('Human Development Index (2021)')) else 0.0,
        "years": years,
        "hdi_history": hdi_history,
        "baselines": {
            "health": float(life_exp_2021) if pd.notna(life_exp_2021) else 70.0,
            "expected_schooling": float(expected_school_2021) if pd.notna(expected_school_2021) else 12.0,
            "mean_schooling": float(mean_school_2021) if pd.notna(mean_school_2021) else 8.0,
            "gni": float(gni_2021) if pd.notna(gni_2021) else 10000.0
        }
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)