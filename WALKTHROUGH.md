# Premium AI Healthcare App Walkthrough

This guide details the features of the upgraded Flask application, which now includes all advanced capabilities from the original prototype, wrapped in a premium, modern UI.

## 🚀 Getting Started

Access the application at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### **First Time Setup:**
1. **Register**: Click "Register here" to create your first account.
2. **Login**: Use your new credentials to enter the secure dashboard.

## ✨ Key Features (New & Upgraded)

### 1. Secure Authentication & Roles
- **Registration**: Full user signup flow with password hashing (`scrypt`).
- **Role-Based Access**: 
    - **Doctors**: Full access to patient history and report generation.
    - **Patients**: Access to personal diagnosis and AI explanations.
- **Session Management**: Secure logout and route protection.

### 2. Live MongoDB Atlas Integration 🍃
- All user data, patient records, and medical history are now stored in **MongoDB Atlas**.
- Data is persistent—your records remain even if the server restarts.
- Automatic fallback to CSV if the database is offline for any reason.

### 3. Personalization
- **Attending Doctor**: Generated reports and patient records now automatically include the name of the logged-in user.
- **User Dashboard**: Displays your specific username and role in the sidebar.

### 4. Direct UI Localization 🌐
- **Instant Switch**: Use the **EN / हिं / ગુજ** buttons in the sidebar to switch the entire app interface instantly.
- **Smart Mapping**: Symptoms and UI labels adapt to your chosen language.

### 5. Patient Prediction History 📜
- **Persistent Log**: Every diagnosis you make is saved securely to your personal history.
- **Visual Analytics**: View symptoms, disease results, and confidence scores in a professional table—exactly like your demo requirements.
- **Actionable Data**: Revisit past screenings anytime without re-entering symptoms.

### 6. Interactive Diagnosis & AI 🧠
- **Gemini AI**: Upgraded to use `models/gemini-flash-latest` for faster, more accurate medical explanations and report generation.
- **Voice Input**: Multi-lingual symptom extraction (English, Hindi, Gujarati).
- **Disease Explanation**: Get detailed breakdowns in multiple languages.

## 🛠️ Files Overview
- `flask_app.py`: Main backend server with MongoDB, AI, and Security logic.
- `templates/register.html`: New secure registration page.
- `templates/login.html`: Updated login portal with detailed error feedback.
- `seed_db.py`: Utility to populate your initial database collections.
- `static/js/script.js`: Frontend logic for real-time symptom extraction and UI updates.

---
*Created with ❤️ for the AI Healthcare Hackathon 2026*
