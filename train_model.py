import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def train():
    print("Loading data...")
    df = pd.read_csv("data/Diseases_and_Symptoms_data.csv")
    
    # Prepare X (features) and y (target)
    X = df.drop("diseases", axis=1)
    y = df["diseases"]
    
    # Encoder
    print("Encoding labels...")
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Save Encoder
    joblib.dump(le, "label_encoder.pkl")
    print("Label Encoder saved.")
    
    # Train Model
    print("Training model...")
    model = ExtraTreesClassifier(n_estimators=100, random_state=42)
    model.fit(X, y_encoded)
    
    # Save Model
    joblib.dump(model, "disease_model.pkl")
    print("Model saved successfully.")
    
    # Test Prediction
    print("\nVerifying model...")
    test_symptom = "pain_chest" # Try to find a valid column
    if test_symptom not in X.columns:
        # Find a random symptom to test
        test_symptom = X.columns[0]
        
    print(f"Testing with symptom: {test_symptom}")
    input_vector = np.zeros(len(X.columns))
    idx = X.columns.get_loc(test_symptom)
    input_vector[idx] = 1
    
    pred = model.predict([input_vector])
    pred_name = le.inverse_transform(pred)[0]
    print(f"Prediction: {pred_name}")

if __name__ == "__main__":
    train()
