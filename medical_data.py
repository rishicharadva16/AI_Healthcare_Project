
# Medical Metadata Database
# Contains: Type, Severity, Emergency Status, Treatment Mode, and Approx Cost (INR)

medical_db = {
    "common cold": {
        "type": "Viral Infection",
        "severity": "Mild",
        "emergency": False,
        "treatment": "Medication & Rest",
        "cost": "₹200 - ₹500",
        "specialist": "General Physician"
    },
    "pneumonia": {
        "type": "Bacterial/Viral Infection",
        "severity": "Moderate to Severe",
        "emergency": True,
        "treatment": "Medication (Antibiotics) or Hospitalization",
        "cost": "₹2,000 - ₹15,000",
        "specialist": "Pulmonologist"
    },
    "heart attack": {
        "type": "Cardiovascular",
        "severity": "Critical",
        "emergency": True,
        "treatment": "Surgery (Angioplasty) & Medication",
        "cost": "₹1,50,000 - ₹4,00,000",
        "specialist": "Cardiologist"
    },
    "asthma": {
        "type": "Respiratory Chronic",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Inhalers & Long-term Medication",
        "cost": "₹1,000 - ₹5,000 (Monthly)",
        "specialist": "Pulmonologist"
    },
    "diabetes": {
        "type": "Endocrine Chronic",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Insulin/Medication & Lifestyle",
        "cost": "₹1,000 - ₹3,000 (Monthly)",
        "specialist": "Endocrinologist"
    },
    "dengue": {
        "type": "Viral Infection",
        "severity": "Moderate to Severe",
        "emergency": True,
        "treatment": "Supportive Care & Fluid Therapy",
        "cost": "₹5,000 - ₹30,000",
        "specialist": "General Physician / Infectious Disease Specialist"
    },
    "typhoid": {
        "type": "Bacterial Infection",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Antibiotics & Diet",
        "cost": "₹2,000 - ₹5,000",
        "specialist": "General Physician"
    },
    "malaria": {
        "type": "Parasitic Infection",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Antimalarial Medication",
        "cost": "₹1,000 - ₹3,000",
        "specialist": "General Physician"
    },
    "migraine": {
        "type": "Neurological",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Medication & Triggers Avoidance",
        "cost": "₹500 - ₹1,500",
        "specialist": "Neurologist"
    },
    "appendicitis": {
        "type": "Digestive Acute",
        "severity": "Severe",
        "emergency": True,
        "treatment": "Surgery (Appendectomy)",
        "cost": "₹30,000 - ₹70,000",
        "specialist": "General Surgeon"
    },
    "gallstone": {
        "type": "Digestive",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Surgery (Cholecystectomy) or Meds",
        "cost": "₹40,000 - ₹90,000",
        "specialist": "Gastroenterologist"
    },
    "kidney stone": {
        "type": "Renal",
        "severity": "Painful/Moderate",
        "emergency": False,
        "treatment": "Lithotripsy/Surgery or Fluids",
        "cost": "₹15,000 - ₹50,000",
        "specialist": "Urologist"
    },
    "hypertension": {
        "type": "Cardiovascular Chronic",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Medication & Lifestyle",
        "cost": "₹500 - ₹1,500 (Monthly)",
        "specialist": "Cardiologist"
    },
    "depression": {
        "type": "Mental Health",
        "severity": "Variable",
        "emergency": False,
        "treatment": "Therapy & Medication",
        "cost": "₹1,000 - ₹5,000 (Per Session/Month)",
        "specialist": "Psychiatrist"
    },
    "arthritis": {
        "type": "Joint Disorder",
        "severity": "Chronic Moderate",
        "emergency": False,
        "treatment": "Physiotherapy & Medication",
        "cost": "₹1,000 - ₹3,000",
        "specialist": "Orthopedist"
    },
    "psoriasis": {
        "type": "Autoimmune Skin",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Topical Creams & Phototherapy",
        "cost": "₹1,000 - ₹5,000",
        "specialist": "Dermatologist"
    },
    "jaundice": {
        "type": "Liver Condition",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Medication & Diet",
        "cost": "₹2,000 - ₹8,000",
        "specialist": "Gastroenterologist"
    },
    "tuberculosis": {
        "type": "Bacterial Infection",
        "severity": "Severe",
        "emergency": False,
        "treatment": "Long-course Antibiotics (DOTS)",
        "cost": "₹5,000 - ₹20,000 (Govt Free)",
        "specialist": "Pulmonologist"
    },
    "anxiety": {
        "type": "Mental Health",
        "severity": "Mild to Severe",
        "emergency": False,
        "treatment": "Therapy & Counseling",
        "cost": "₹1,000 - ₹3,000 (Per Session)",
        "specialist": "Psychologist"
    },
    "carpal tunnel syndrome": {
        "type": "Nerve Compression",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Splinting & Therapy",
        "cost": "₹5,000 - ₹15,000",
        "specialist": "Orthopedist / Neurologist"
    },
    "hyperemesis gravidarum": {
        "type": "Pregnancy Complication",
        "severity": "Severe",
        "emergency": True,
        "treatment": "IV Fluids & anti-nausea medication",
        "cost": "₹10,000 - ₹50,000",
        "specialist": "Obstetrician"
    },
    "appendicitis": {
        "type": "Acute Inflammation",
        "severity": "Critical",
        "emergency": True,
        "treatment": "Surgical Removal",
        "cost": "₹30,000 - ₹1,00,000",
        "specialist": "General Surgeon"
    },
    "malaria": {
        "type": "Parasitic Infection",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Antimalarial Meds",
        "cost": "₹1,000 - ₹5,000",
        "specialist": "General Physician"
    },
    "dengue": {
        "type": "Viral Infection",
        "severity": "Severe",
        "emergency": True,
        "treatment": "Fluids & Monitoring",
        "cost": "₹5,000 - ₹40,000",
        "specialist": "General Physician"
    },
    "typhoid": {
        "type": "Bacterial Infection",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Antibiotics",
        "cost": "₹2,000 - ₹8,000",
        "specialist": "General Physician"
    },
    "asthma": {
        "type": "Respiratory",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Inhalers",
        "cost": "₹1,000 - ₹4,000",
        "specialist": "Pulmonologist"
    },
    "migraine": {
        "type": "Neurological",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Medication & Rest",
        "cost": "₹500 - ₹2,000",
        "specialist": "Neurologist"
    },
    "pneumonia": {
        "type": "Lung Infection",
        "severity": "Severe",
        "emergency": True,
        "treatment": "Antibiotics / Oxygen",
        "cost": "₹10,000 - ₹60,000",
        "specialist": "Pulmonologist"
    },
    "common cold": {
        "type": "Viral",
        "severity": "Mild",
        "emergency": False,
        "treatment": "Rest & Fluids",
        "cost": "₹200 - ₹500",
        "specialist": "General Physician"
    },
    "psoriasis": {
        "type": "Skin Autoimmune",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Topical Creams",
        "cost": "₹1,000 - ₹10,000",
        "specialist": "Dermatologist"
    },
    "urinary tract infection": {
        "type": "Bacterial",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Antibiotics",
        "cost": "₹1,000 - ₹3,000",
        "specialist": "General Physician"
    },
    "hepatitis a": {
        "type": "Viral Liver",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Rest & Nutrition",
        "cost": "₹2,000 - ₹10,000",
        "specialist": "Hepatologist"
    },
    "gerd": {
        "type": "Digestive",
        "severity": "Mild to Moderate",
        "emergency": False,
        "treatment": "Antacids & Lifestyle",
        "cost": "₹500 - ₹3,000",
        "specialist": "Gastroenterologist"
    },
    # Add defaults for others to prevent crashes
    "default": {
        "type": "Medical Condition",
        "severity": "Moderate",
        "emergency": False,
        "treatment": "Consult a Doctor",
        "cost": "Consult Doctor",
        "specialist": "General Physician"
    }
}

def get_medical_info(disease_name):
    # Normalize key
    key = disease_name.lower().strip()
    # Try exact match
    if key in medical_db:
        return medical_db[key]
    
    # Try partial match (e.g., "acute pancreatitis" -> find "pancreatitis" if it existed, or reverse)
    # Simple fallback for now
    return medical_db["default"]
