import pandas as pd

def analyze():
    df = pd.read_csv("data/Diseases_and_Symptoms_data.csv")
    
    targets = ["Dengue", "injury to the trunk", "Influenza", "Chicken pox"]
    
    for t in targets:
        # Case insensitive match
        row = df[df['diseases'].str.lower() == t.lower()]
        if not row.empty:
            print(f"\n--- {t} ---")
            # Get columns where value is 1
            symptoms = row.iloc[0].drop('diseases')
            active_symptoms = symptoms[symptoms == 1].index.tolist()
            print(active_symptoms)
        else:
            print(f"\n{t} not found in dataset.")

if __name__ == "__main__":
    analyze()
