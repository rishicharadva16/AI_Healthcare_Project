import joblib
import pandas as pd
import numpy as np

def verify():
    # Load model and data
    try:
        model = joblib.load("disease_model.pkl")
        le = joblib.load("label_encoder.pkl")
        df = pd.read_csv("data/Diseases_and_Symptoms_data.csv")
        symptoms_list = df.drop("diseases", axis=1).columns.tolist()
    except Exception as e:
        print(f"Error loading: {e}")
        return

    # Test Case: Fever, Headache, Bones are painful (Dengue/Flu?)
    # Note: "bones are painful" is the column name in the dataset? Need to check.
    # Looking at previous user image: "bones are painful" is a symptom chip.
    
    test_symptoms = ["fever", "headache", "bones are painful"]
    
    # Check if they exist in symptoms_list
    valid_symptoms = [s for s in test_symptoms if s in symptoms_list]
    print(f"Testing with: {valid_symptoms}")
    
    input_vector = np.zeros(len(symptoms_list))
    for s in valid_symptoms:
        idx = symptoms_list.index(s)
        input_vector[idx] = 1
        
    # Predict
    probs = model.predict_proba([input_vector])[0]
    top_indices = np.argsort(probs)[-5:][::-1]
    
    print("\nTop 5 Predictions:")
    for idx in top_indices:
        prob = probs[idx]
        if prob > 0.01:
            disease = le.inverse_transform([idx])[0]
            print(f"{disease}: {prob*100:.2f}%")

if __name__ == "__main__":
    verify()
