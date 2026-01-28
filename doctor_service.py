import json
import os
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Global cache for doctor data
DOCTORS_DATA = None
DATA_PATH = os.path.join("data", "Doctors_Data.json")

# Disease to Specialist Mapping
SPECIALIST_MAPPING = {
    # Cardiology
    "heart attack": "Cardiologist",
    "chest pain": "Cardiologist",
    "hypertension": "Cardiologist",
    "coronary artery disease": "Cardiologist",
    
    # Dermatology
    "fungal infection": "Dermatologist",
    "allergy": "Dermatologist",
    "drug reaction": "Dermatologist",
    "acne": "Dermatologist",
    "psoriasis": "Dermatologist",
    "impetigo": "Dermatologist",
    "chicken pox": "General Physician", 
    "skin infection": "Dermatologist",
    
    # Endocrinology
    "diabetes": "Diabetologist",
    "hypoglycemia": "Diabetologist",
    "hypothyroidism": "Endocrinologist",
    "hyperthyroidism": "Endocrinologist",
    
    # Gastroenterology
    "gerd": "Gastroenterologist",
    "chronic cholestasis": "Gastroenterologist",
    "peptic ulcer diseae": "Gastroenterologist",
    "jaundice": "Gastroenterologist",
    "alcoholic hepatitis": "Gastroenterologist",
    "hepatitis": "Gastroenterologist",
    
    # Neurology
    "migraine": "Neurologist",
    "paralysis (brain hemorrhage)": "Neurologist",
    "cervical spondylosis": "Neurologist",
    
    # Orthopedics
    "osteoarthristis": "Orthopedist",
    "arthritis": "Orthopedist",
    
    # Pulmonology
    "bronchial asthma": "Pulmonologist",
    "pneumonia": "Pulmonologist",
    "tuberculosis": "Pulmonologist",
    
    # General / Infectious
    "malaria": "General Physician",
    "dengue": "General Physician",
    "typhoid": "General Physician",
    "common cold": "General Physician",
    "fever": "General Physician",
    
    # Gynecology
    "hyperemesis gravidarum": "Obstetrician",
    "pcos": "Gynecologist"
}

def load_data():
    global DOCTORS_DATA
    if DOCTORS_DATA:
        return DOCTORS_DATA
        
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            DOCTORS_DATA = data.get("Doctor", [])
            print(f"Loaded {len(DOCTORS_DATA)} doctors.")
    except Exception as e:
        print(f"Error loading doctor data: {e}")
        DOCTORS_DATA = []
        
    return DOCTORS_DATA

def normalize_city(city_str):
    """
    Extracts the English city name from strings like 'Ahmedabad (અમદાવાદ)'
    Returns lowercase normalized city.
    """
    if not city_str:
        return ""
    # Remove contents in parenthesis including parenthesis
    city_str = re.sub(r'\(.*?\)', '', city_str)
    return city_str.strip().lower()

def get_city_from_coords(lat, lng):
    """
    Reverse geocodes latitude and longitude to find the city.
    """
    try:
        geolocator = Nominatim(user_agent="healthcare_ai_app")
        location = geolocator.reverse(f"{lat}, {lng}", language="en", timeout=10)
        
        if location and location.raw.get('address'):
            address = location.raw['address']
            # Try to find city, then town, then village, then county
            city = address.get('city') or address.get('town') or address.get('village') or address.get('county')
            if city:
                return city
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None

def find_doctors_for_disease(lat, lng, disease_name):
    """
    Main entry point.
    1. Detects city from coords.
    2. Determines specialist from disease.
    3. Filters doctors.
    """
    
    # 1. Identify User City
    user_city = get_city_from_coords(lat, lng)
    if not user_city:
        return {"error": "Could not detect location. Please enable location services.", "doctors": []}
        
    normalized_user_city = user_city.lower()
    
    # 2. Determine Specialist
    needed_specialist = "General Physician"
    # Basic fuzzy match or direct lookup
    disease_lower = disease_name.lower().strip()
    
    # Direct match
    if disease_lower in SPECIALIST_MAPPING:
        needed_specialist = SPECIALIST_MAPPING[disease_lower]
    else:
        # Partial match
        for key, val in SPECIALIST_MAPPING.items():
            if key in disease_lower:
                needed_specialist = val
                break
                
    print(f"Logic: User City='{user_city}', Disease='{disease_name}' -> Specialist='{needed_specialist}'")
    
    # 3. Filter Doctors
    doctors = load_data()
    
    # Strategy:
    # A. Perfect Match: City + Specialist
    # B. Fallback 1: City + 'Doctor' (Generic)
    # C. Fallback 2: Nearby City (Not implemented strictly, just showing 'Others')
    
    perfect_matches = []
    city_fallbacks = []
    
    for doc in doctors:
        doc_city = normalize_city(doc.get('city', ''))
        doc_spec = doc.get('specialization', '').strip()
        
        # Check City Match
        # We check if user city is in doc city or vice versa to handle variances
        is_city_match = (normalized_user_city in doc_city) or (doc_city in normalized_user_city)
        
        if is_city_match:
            # Check Specialist
            if needed_specialist.lower() in doc_spec.lower():
                perfect_matches.append(doc)
            elif "doctor" in doc_spec.lower() or "physician" in doc_spec.lower():
                city_fallbacks.append(doc)
                
    # Prioritize results
    final_list = perfect_matches if perfect_matches else city_fallbacks
    
    # Limit results
    return {
        "status": "success",
        "city_detected": user_city,
        "specialist_required": needed_specialist,
        "count": len(final_list),
        "doctors": final_list[:10] # Top 10
    }
