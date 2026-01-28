import pandas as pd
import joblib

# Load data to get unique diseases
df = pd.read_csv("data/Diseases_and_Symptoms_data.csv")
diseases = df['diseases'].unique()

print("List of Diseases:")
for d in diseases:
    print(d)
