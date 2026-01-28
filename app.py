import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import os
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO
import ast # Added for parsing list strings
import soundfile as sf
import tempfile
import openai
import json
import speech_recognition as sr # Added for voice input
import time # Added for potential future use or specific timing needs

# ================= FAST IMPORTS =================
# Removed languages.py import as per instruction

# ================= VOICE PROCESSING FUNCTION =================

from deep_translator import GoogleTranslator
translator = GoogleTranslator()

# Load Translations from JSON
@st.cache_data
def load_translations():
    """Loads translations from the JSON file."""
    json_path = "data/symptom_translations.json"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading translations: {e}")
        return {}

# Load translations once
TRANSLATIONS = load_translations()

def process_voice_symptoms_fallback(text, symptoms_list, language_code):
    """
    Fallback method: Detects symptoms using keyword matching (No AI).
    """
    detected_symptoms = set()
    text = text.lower().strip()
    
    # 2. Key-based Lookup
    lang_key = language_code.split("-")[0] # e.g. "hi"
    
    if lang_key in TRANSLATIONS:
        lang_map = TRANSLATIONS[lang_key]
        if text in lang_map:
            detected_symptoms.add(lang_map[text])
        else:
             for key, value in lang_map.items():
                 if key in text:
                     detected_symptoms.add(value)

    # 3. English Match
    if text in symptoms_list:
        detected_symptoms.add(text)
    for sym in symptoms_list:
        if sym in text:
             detected_symptoms.add(sym)
             
    return detected_symptoms

def process_voice_symptoms(text, symptoms_list, language_code):
    """
    Detects symptoms from spoken text using OpenAI GPT-4o, with fallback.
    """
    detected_symptoms = set()
    used_fallback = False
    
    # Create the prompt with the official symptom list
    symptoms_str = ", ".join(symptoms_list)
    
    system_prompt = f"""You are an expert medical symptom extractor.
The patient may speak in Gujarati, Hindi, or English.
First, understand and translate the sentence to English if needed.
Then extract symptoms ONLY from this official symptom list:

{symptoms_str}

Rules:
- Output ONLY a Python-style list like ["fever", "vomiting"]
- Do NOT explain anything
- Do NOT invent symptoms
- If nothing matches, return []
"""

    user_message = f"""Patient voice text:
"{text}"
"""

    try:
        with st.spinner("🤖 Analyzing symptoms with AI..."):
             response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.0
            )
             
        content = response.choices[0].message.content.strip()
        
        # Simple cleanup
        if "```" in content:
            content = content.replace("```python", "").replace("```json", "").replace("```", "")
        
        extracted_list = ast.literal_eval(content)
        
        if isinstance(extracted_list, list):
            detected_symptoms = set(extracted_list)
        else:
            raise ValueError("Invalid format from AI")
            
    except Exception as e:
        st.error(f"⚠️ AI limit reached (Using Basic Match): {e}")
        detected_symptoms = process_voice_symptoms_fallback(text, symptoms_list, language_code)
        used_fallback = True

    # Update Session State (Buffer Pattern)
    if detected_symptoms:
        if "pending_symptoms" not in st.session_state:
             st.session_state.pending_symptoms = []
        
        current_pending = set(st.session_state.pending_symptoms)
        current_selected = set(st.session_state.symptoms) if "symptoms" in st.session_state else set()
        
        # Merge
        new_pending = current_pending.union(current_selected).union(detected_symptoms)
        
        st.session_state.pending_symptoms = list(new_pending)
        st.session_state.voice_detected = list(detected_symptoms)
        st.session_state.ask_confirm = True 
        
        msg = "✅ AI Detected" if not used_fallback else "✅ Basic Match Detected"
        st.success(f"{msg}: {', '.join(detected_symptoms)}")
    else:
        st.warning("⚠️ No matching symptoms found.")


# For Voice Input (Feature 3)
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False

# For PDF Generation (Feature 4)
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- OPENAI CLIENT ----------------
# WARNING: Ideally, use st.secrets["OPENAI_API_KEY"] for security. 
client = OpenAI(api_key="YOUR_API_KEY_HERE")

st.set_page_config(page_title="AI Rural Health System", layout="wide")

st.info("⚕️ This system is for early screening only and does not replace a certified medical doctor.")

# ---------------- FAST CACHED LOADING ----------------
@st.cache_resource
def load_model():
    import gc
    gc.collect()
    # Use mmap_mode='r' to prevent loading entire model into RAM at once
    model = joblib.load("disease_model.pkl", mmap_mode='r')
    le = joblib.load("label_encoder.pkl")
    data = pd.read_csv("data/Diseases_and_Symptoms_data.csv")
    symptoms = data.drop("diseases", axis=1).columns
    return model, le, symptoms, data # Return data too

model, le, symptoms_list, df_symptoms = load_model() # Unpack data

desc = pd.read_csv("data/description.csv")
prec = pd.read_csv("data/precautions.csv")
meds = pd.read_csv("data/medications.csv")
diet = pd.read_csv("data/diets.csv")
work = pd.read_csv("data/workout.csv")

# ---------------- LANGUAGE ----------------
lang = st.sidebar.selectbox("Language / ભાષા", ["English", "Gujarati"])

t = {
    "English": {"title": "AI Multi-Disease Diagnostic Assistant","login": "Login","username": "Username","password": "Password","symptoms": "Select your symptoms","predict": "Predict Disease","result": "Prediction Result","logout": "Logout"},
    "Gujarati": {"title": "AI બહુ-રોગ નિદાન સહાયક","login": "લૉગિન","username": "વપરાશકર્તા નામ","password": "પાસવર્ડ","symptoms": "તમારા લક્ષણો પસંદ કરો","predict": "રોગ શોધો","result": "નિદાન પરિણામ","logout": "લૉગઆઉટ"}
}[lang]

# ---------------- LOGIN SYSTEM ----------------
if "user" not in st.session_state:
    st.session_state.user = None

for k in ["last_disease","last_conf","last_symptoms","ai_explanation","ai_gujarati","ai_report","image_result","image_gujarati"]:
    if k not in st.session_state:
        st.session_state[k] = ""

def login():
    st.title(t["login"])
    username = st.text_input(t["username"])
    password = st.text_input(t["password"], type="password")

    if st.button(t["login"]):
        users = pd.read_csv("users.csv")
        users.columns = users.columns.str.strip().str.lower()
        if ((users["username"] == username) & (users["password"] == password)).any():
            st.session_state.user = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

if st.session_state.user is None:
    login()
    st.stop()

# ----------------- SESSION STATE INIT -----------------
keys = [
    "user", "last_disease", "last_conf", "last_symptoms",
    "ai_explanation", "ai_gujarati", "ai_report",
    "image_result", "image_gujarati"
]
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = "" if "ai" in k or "image" in k else None


# 🔥🔥🔥 ADD STEP 1 EXACTLY HERE (JUST BELOW THIS) 🔥🔥🔥

if "symptoms" not in st.session_state:
    st.session_state.symptoms = []

if "voice_detected" not in st.session_state:
    st.session_state.voice_detected = []

if "pending_symptoms" not in st.session_state:
    st.session_state.pending_symptoms = []

# --- SYNC BUFFER TO WIDGET STATE BEFORE WIDGET CREATION ---
if st.session_state.pending_symptoms:
    # This runs BEFORE st.multiselect is created
    # We overwrite the widget key 'symptoms' safely here
    st.session_state.symptoms = list(set(st.session_state.pending_symptoms))
    st.session_state.pending_symptoms = [] # Clear buffer


if "spoken_text" not in st.session_state:
    st.session_state.spoken_text = ""

if "auto_predict" not in st.session_state:
    st.session_state.auto_predict = False

if "ask_confirm" not in st.session_state:
    st.session_state.ask_confirm = False

# --- NEW STATE FOR INTERACTIVE CHECKER ---
if "step" not in st.session_state:
    st.session_state.step = "Input" # Input -> Refinement -> Final
if "candidates" not in st.session_state:
    st.session_state.candidates = []
if "asked_symptoms" not in st.session_state:
    st.session_state.asked_symptoms = []
if "final_result" not in st.session_state:
    st.session_state.final_result = None


# ---------------- SIDEBAR ----------------
st.sidebar.write("Logged in as:", st.session_state.user)

if st.sidebar.button(t["logout"]):
    st.session_state.clear()
    st.rerun()

if st.sidebar.button("🧹 Clear All Results"):
    for k in [
        "last_disease","last_conf","last_symptoms",
        "ai_explanation","ai_gujarati","ai_report",
        "image_result","image_gujarati",
        "voice_detected","spoken_text","symptoms","ask_confirm"
    ]:
        if k in st.session_state:
            st.session_state[k] = "" if isinstance(st.session_state[k], str) else []

    st.success("✅ Everything cleared successfully")
    st.rerun()

mode = st.sidebar.selectbox("Diagnosis Mode", ["⚡ Fast Mode (Common Diseases)", "🧠 Extended Mode (All Diseases)"])

# ================= MAIN APP =================
st.title("🩺 " + t["title"])

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🦠 Prediction",
    "🤖 Explain (English)",
    "🇮🇳 Explain (Gujarati)",
    "📄 Medical Report",
    "📷 Image Diagnosis",
    "📖 Dictionary" # New Tab
])

# ---------------- HELPER FUNCTIONS ----------------

def get_discriminating_symptom(candidates, current_symptoms, asked_symptoms, data):
    """Finds the symptom that best distinguishes between the candidate diseases."""
    try:
        # Filter data for candidate diseases
        subset = data[data['diseases'].isin(candidates)]
        
        if subset.empty:
            return None
            
        # Calculate symptom frequencies for these diseases
        # (Assuming dataset has 1s and 0s, mean gives probability/frequency)
        symptom_stats = subset.drop('diseases', axis=1).mean()
        
        best_symptom = None
        max_variance = -1
        
        for symptom, freq in symptom_stats.items():
            # Skip if already known
            if symptom in current_symptoms or symptom in asked_symptoms:
                continue
                
            # We want a symptom that is present in some (~1.0) and absent in others (~0.0)
            # Variance or simply closer to 0.5 mean generally implies split
            # But specific to candidates:
            # Let's verify variance across the *individual* candidate means
            
            # Group by disease to get the "typical profile" for each candidate
            disease_profiles = subset.groupby('diseases')[symptom].mean()
            variance = disease_profiles.var()
            
            if pd.isna(variance): variance = 0
            
            if variance > max_variance:
                max_variance = variance
                best_symptom = symptom
                
        return best_symptom
    except Exception as e:
        st.error(f"Logic Error: {e}")
        return None
def clear_on_symptom_change():
    # Do NOT clear voice detected when autofilling
    st.session_state.last_disease = None
    st.session_state.last_conf = None
    st.session_state.ai_explanation = ""
    st.session_state.ai_gujarati = ""
    st.session_state.ai_report = ""

def confirm_symptoms_callback():
    """Callback to update symptoms state safely before rerun"""
    if "voice_detected" in st.session_state:
        st.session_state.symptoms = st.session_state.voice_detected
    if "voice_detected" in st.session_state:
        st.session_state.symptoms = st.session_state.voice_detected
    st.session_state.ask_confirm = False

def reset_app():
    """Callback to safely reset the state"""
    st.session_state.step = "Input"
    st.session_state.symptoms = []
    st.session_state.logic_symptoms = []
    st.session_state.asked_symptoms = []
    st.session_state.voice_detected = []
    st.session_state.final_result = None

def update_symptoms_state():
    """Helper to update symptoms state and force rerun only if needed"""
    if "pending_symptoms" in st.session_state and st.session_state.pending_symptoms:
        st.session_state.symptoms = st.session_state.pending_symptoms
        st.session_state.pending_symptoms = None
        # st.rerun() # Might not be needed if called before widget

# Specialist mapping (Feature 1)
def recommend_specialist(disease):
    mapping = {
        "heart": "Cardiologist",
        "skin": "Dermatologist",
        "diabetes": "Endocrinologist",
        "asthma": "Pulmonologist",
        "brain": "Neurologist",
        "infection": "General Physician"
    }
    for k, v in mapping.items():
        if k in disease.lower():
            return v
    return "General Physician"

# ================= TAB 1 — PREDICTION =================
with tab1:

    col1, col2 = st.columns([2,1])

    with col1:
        # Apply voice detected symptoms BEFORE widget loads
        default_symptoms = st.session_state.voice_detected if st.session_state.voice_detected else []

        selected_symptoms = st.multiselect(
            t["symptoms"],
            options=list(symptoms_list),
            default=default_symptoms,
            key="symptoms",
            on_change=clear_on_symptom_change   
        )


# 🎤 Voice Input Feature (FINAL WORKING VERSION)

if VOICE_AVAILABLE:

    if "spoken_text" not in st.session_state:
        st.session_state.spoken_text = ""

    st.write("### 🎙️ Voice Input")
    
    # User Request: Manual Language Selection (Static)
    lang_options = {
        "English (India)": "en-IN",
        "Hindi": "hi-IN",
        "Gujarati": "gu-IN"
    }
    
    voice_lang = st.radio(
        "Select Voice Language:",
        list(lang_options.keys()),
        index=0,
        horizontal=True
    )
    
    selected_code = lang_options[voice_lang]

    if st.button("🎤 Speak Symptoms"):

        r = sr.Recognizer()

        with sr.Microphone() as source:
            st.info(f"🎧 Listening in {voice_lang}... Speak your symptoms clearly")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=15)
            except sr.WaitTimeoutError:
                st.error("⏳ Listening timed out. Please speak again.")
                st.stop()

        # Use selected language code directly
        text = ""
        try:
            text = r.recognize_google(audio, language=selected_code)
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio")
        except sr.RequestError as e:
            st.error(f"❌ Could not request results; {e}")

        if text:
            st.success(f"🗣️ Recognized: **{text}**")
            st.session_state.spoken_text = text
            process_voice_symptoms(text, symptoms_list, selected_code)
        else:
             st.warning("⚠️ No speech detected.")


    # 🔥 Button to convert spoken text → symptoms
    if st.session_state.spoken_text:

        st.info("Click below to detect symptoms from your voice 👇")

        if st.button("🔍 Detect Symptoms from Voice"):

            # Use the unified function instead of repeating logic
            process_voice_symptoms(st.session_state.spoken_text, symptoms_list, selected_code)


        # Show warning if it exists
        if "voice_warning" in st.session_state and st.session_state.voice_warning:
            st.warning(st.session_state.voice_warning)
            del st.session_state.voice_warning

        st.button("✅ Use Voice Symptoms", on_click=process_voice_symptoms, args=(st.session_state.spoken_text, symptoms_list, selected_code))

        if "ask_confirm" not in st.session_state:
            st.session_state.ask_confirm = False

        if st.session_state.ask_confirm:

            st.warning("❓ Are these symptoms correct?")

            col_yes, col_no = st.columns(2)

            with col_yes:
                if st.button("✅ Yes, Predict Now", on_click=confirm_symptoms_callback):
                    st.rerun()

            with col_no:
                if st.button("❌ No, Speak Again"):
                    st.session_state.spoken_text = ""
                    st.session_state.voice_detected = []
                    st.session_state.ask_confirm = False
                    st.warning("🎤 Please speak again")


    with col2:
        age = st.number_input("Age", 1, 120, 30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    input_data = [1 if s in selected_symptoms else 0 for s in symptoms_list]

    
    # ================= INTERACTIVE SYMPTOM CHECKER LOGIC =================
    
    # 1. INPUT PHASE
    if st.session_state.step == "Input":
        if st.button("🔍 " + t["predict"]):
            
            # 🔥 MERGE MANUAL & VOICE SYMPTOMS
            # Use local variable for logic, do NOT write to st.session_state.symptoms (Widget Key)
            final_symptoms = list(set(selected_symptoms + st.session_state.voice_detected))
            
            # DEBUG: Print symptoms to console/UI to allow debugging
            st.write(f"🛑 DEBUG: Final Symptoms: {final_symptoms}")

            if not final_symptoms:
                st.warning("⚠️ Please select or speak at least one symptom.")
            else:
                # Save to a generic persistent state for the wizard flow
                st.session_state.logic_symptoms = final_symptoms
                
                # Check for exact matches in symptoms_list
                # Clean up symptoms_list for robust matching
                clean_symptoms_list = [s.strip().lower() for s in symptoms_list]
                # Normalize user symptoms too
                final_symptoms_clean = [s.strip().lower() for s in final_symptoms]
                
                input_data = [1 if s in final_symptoms_clean else 0 for s in clean_symptoms_list]
                
                st.write(f"🛑 DEBUG: Input Data Sum: {sum(input_data)}")
                
                X = np.array(input_data).reshape(1, -1)
                
                # Get Probabilities
                probs = model.predict_proba(X)[0]
                
                # Get Top 3 Candidates
                top_indices = np.argsort(probs)[-3:][::-1]
                candidates = []
                for idx in top_indices:
                    prob = probs[idx]
                    if prob > 0.05: # Filter noise
                        candidates.append((le.classes_[idx], prob))
                        
                st.session_state.candidates = candidates
                
                # Check Confidence
                if not candidates:
                     st.warning("No disease matches found.")
                else:
                    top_prob = candidates[0][1]
                    if top_prob > 0.9 or len(candidates) == 1:
                        # High confidence -> Go directly to Final
                        st.session_state.final_result = candidates[0][0]
                        st.session_state.step = "Final"
                        st.rerun()
                    else:
                        # Low confidence -> Ask Questions
                        st.session_state.step = "Refinement"
                        st.rerun()

    # 2. REFINEMENT PHASE (Interactive Questions)
    elif st.session_state.step == "Refinement":
        
        # Display Candidates (User requested transparency)
        c_names = [c[0] for c in st.session_state.candidates]
        st.info(f"🔎 We are considering: **{', '.join(c_names)}**")
        
        # Find Next Question
        # data_df = pd.read_csv("data/Diseases_and_Symptoms_data.csv") # Removed slow read
        
        # Use session state symptoms or what we have gathered so far
        # We need to rely on what was passed from input phase. 
        # Since we couldn't save to `st.session_state.symptoms` in step 1 due to the error,
        # we might have lost the combined list if we didn't save it elsewhere!
        
        # FIX: We need a persistent storage that ISN'T the widget key.
        # Let's use `st.session_state.logic_symptoms` for the algorithm steps.
        
        if "logic_symptoms" not in st.session_state or st.session_state.step == "Input":
             # Initialize from whatever the widget has + voice on first entry
             # But wait, step "Input" logic block is where we tried to set it.
             pass

        # Recover logic symptoms if missing (should be set in Input block, see below fix)
        current_logic_symptoms = st.session_state.get("logic_symptoms", [])
        
        next_symptom = get_discriminating_symptom(c_names, current_logic_symptoms, st.session_state.asked_symptoms, df_symptoms)
        
        if next_symptom:
            st.write(f"### ❓ Do you also experience: **{next_symptom}**?")
            
            col_y, col_n, col_skip = st.columns(3)
            
            if col_y.button("✅ Yes, I have it"):
                st.session_state.logic_symptoms.append(next_symptom)
                st.session_state.asked_symptoms.append(next_symptom)
                st.rerun()
                
            if col_n.button("❌ No, I don't"):
                st.session_state.asked_symptoms.append(next_symptom)
                st.rerun()
                
            if col_skip.button("⏩ Skip / Show Result"):
                st.session_state.step = "Final"
                # Pick top candidate
                st.session_state.final_result = st.session_state.candidates[0][0]
                st.rerun()
        else:
            # No more questions
            st.session_state.step = "Final"
            st.session_state.final_result = st.session_state.candidates[0][0]
            st.rerun()

    # 3. FINAL RESULT PHASE
    elif st.session_state.step == "Final":
        
        disease = st.session_state.final_result
        st.session_state.last_disease = disease # For other tabs
        
        # --- RICH MEDICAL REPORT ---
        # from medical_data import get_medical_info # Already imported
        # We need to make sure medical_data is imported if not already at top
        from medical_data import get_medical_info 
        
        info = get_medical_info(disease)
        
        st.success(f"## 🩺 Diagnosis: {disease}")
        
        # Metadata Cards
        m1, m2, m3 = st.columns(3)
        m1.metric("Severity", info["severity"], delta_color="inverse")
        m2.metric("Type", info["type"])
        m3.metric("Emergency?", "YES 🚨" if info["emergency"] else "No ✅")
        
        c1, c2 = st.columns(2)
        c1.info(f"**💊 Treatment:** {info['treatment']}")
        c2.warning(f"**💰 Approx Cost:** {info['cost']}")
        
        st.divider()
        st.write("### 👨‍⚕️ Specialist to Consult")
        st.write(f"**{info['specialist']}**")
        
        # Load Existing CSV Data (Meds, Precautions)
        try:
            d_lower = disease.strip().lower()
            
            # Precautions
            prec_match = prec[prec['Disease'].str.strip().str.lower() == d_lower]
            if not prec_match.empty:
                st.write("### 🛡️ Precautions")
                p_row = prec_match.iloc[0]
                st.write(f"- {p_row['Precaution_1']}")
                st.write(f"- {p_row['Precaution_2']}")
                st.write(f"- {p_row['Precaution_3']}")
        except:
            pass
            
        if st.button("🔄 Start Over", on_click=reset_app):
            st.rerun()



# ================= TAB 2 — EXPLAIN ENGLISH =================
with tab2:
    st.subheader("🤖 Disease Explanation (English)")

    if st.session_state.last_disease:
        if st.button("Explain Disease (AI)"):
            with st.spinner("AI doctor is explaining..."):
                prompt = f"Explain the disease {st.session_state.last_disease} in simple language with precautions."
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                st.session_state.ai_explanation = res.choices[0].message.content

        if st.session_state.ai_explanation:
            st.info(st.session_state.ai_explanation)
    else:
        st.warning("⚠️ Please predict a disease first.")

# ================= TAB 3 — GUJARATI =================
with tab3:
    st.subheader("🇮🇳 રોગની સમજાવટ (Gujarati)")

    if st.session_state.last_disease:
        if st.button("Explain in Gujarati (AI)"):
            with st.spinner("AI translating..."):
                prompt = f"Explain the disease {st.session_state.last_disease} in very simple Gujarati."
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                st.session_state.ai_gujarati = res.choices[0].message.content

        if st.session_state.ai_gujarati:
            st.success(st.session_state.ai_gujarati)
    else:
        st.warning("⚠️ Please predict a disease first.")

# ================= TAB 4 — MEDICAL REPORT =================
with tab4:
    st.subheader("📄 AI Medical Report")

    if st.session_state.last_disease:
        if st.button("Generate Medical Report (AI)"):
            with st.spinner("Generating report..."):
                prompt = f"Create a medical screening report for disease {st.session_state.last_disease}."
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
                st.session_state.ai_report = res.choices[0].message.content

        if st.session_state.ai_report:
            st.text_area("Generated Report", st.session_state.ai_report, height=300)

            # 📄 PDF Download Feature (Feature 4)
            pdf_file = "medical_report.pdf"
            doc = SimpleDocTemplate(pdf_file)
            styles = getSampleStyleSheet()
            story = [Paragraph(st.session_state.ai_report, styles["BodyText"])]
            doc.build(story)

            with open(pdf_file, "rb") as f:
                st.download_button("⬇️ Download Report (PDF)", f, file_name="Medical_Report.pdf")
    else:
        st.warning("⚠️ Please predict a disease first.")

# ================= TAB 5 — IMAGE DIAGNOSIS =================
with tab5:
    st.subheader("📷 Image Based Diagnosis")

    uploaded_file = st.file_uploader("Upload disease / scan / report image", type=["jpg","jpeg","png"])

    if uploaded_file is None:
        st.session_state.image_result = ""

    def encode_image(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300)

        if st.button("🔍 Analyze Image (AI)"):
            with st.spinner("Analyzing image..."):
                base64_image = encode_image(image)
                prompt = "Analyze this medical image or report and suggest possible condition and advice."

                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                        ]
                    }]
                )

                st.session_state.image_result = res.choices[0].message.content

        if st.session_state.image_result:
            st.info(st.session_state.image_result)

# ================= TAB 6 — DICTIONARY =================
with tab6:
    st.subheader("📖 Symptom & Disease Dictionary")
    st.markdown("Search for symptoms in **English, Hindi, and Gujarati**.")

    # Load translations dynamically
    translations = load_translations()
    
    # Prepare data for the table
    dict_data = []

    # 1. Add Symptoms from JSON
    # We iterate through the 'hi' keys as the base, assuming 'gu' has similar keys
    # or we just list everything we find.
    # To make it clean, let's use the 'hi' keys
    
    if "hi" in translations:
        for term, eng_term in translations["hi"].items():
            
            # Try to find Gujarati equivalent
            guj_term = "N/A"
            if "gu" in translations:
                # We need to find the key in 'gu' that maps to the SAME English term
                # This reverse lookup is O(N) but okay for small datasets. 
                # Better: The JSON structure is { "lang": { "foreign": "english" } }
                # So we have "foreign" -> "english".
                # To show a table, we want: English | Hindi | Gujarati
                
                # We already have English (eng_term) and Hindi (term).
                # Let's find Gujarati for this eng_term.
                for g_k, g_v in translations["gu"].items():
                    if g_v.lower() == eng_term.lower():
                        guj_term = g_k
                        break
            
            dict_data.append({
                "English": eng_term.title(),
                "Hindi": term,
                "Gujarati": guj_term
            })
            
    # Convert to DataFrame
    df_dict = pd.DataFrame(dict_data)
    
    # Search Bar
    search_query = st.text_input("🔍 Search Dictionary", "")
    
    if not df_dict.empty:
        if search_query:
            mask = df_dict.apply(lambda x: x.astype(str).str.contains(search_query, case=False)).any(axis=1)
            df_display = df_dict[mask]
        else:
            df_display = df_dict
            
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("Dictionary is empty or could not be loaded.")

# ---------------- HISTORY ----------------
st.sidebar.subheader("📜 Patient History")

if st.sidebar.button("View History"):
    hist = pd.read_csv("patient_history.csv")
    user_hist = hist[hist["username"] == st.session_state.user]
    st.dataframe(user_hist)

