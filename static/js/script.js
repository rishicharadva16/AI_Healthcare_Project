// State
let selectedSymptoms = [];
let askedSymptoms = [];
let currentVoiceText = "";
let currentLang = 'en';
let reportLang = 'English';
let SYMPTOM_MAP = {}; // Map of lang -> { EnglishSym: LocalSym }

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const res = await apiFetch('/api/symptom_map');
        if (res) {
            SYMPTOM_MAP = await res.json();
            console.log("Symptom Map Loaded");
            renderSymptomDropdown();
        }
    } catch (e) {
        console.error("Map Load Error:", e);
    }
});

const UI_STRINGS = {
    'en': {
        'app-name': 'HealthAI', 'logout': 'Logout', 'nav-diagnosis': 'Diagnosis',
        'nav-explain': 'Explain Disease', 'nav-report': 'Medical Report',
        'nav-image': 'Image Analysis', 'nav-dictionary': 'Dictionary',
        'nav-history': 'Patient History', 'diag-title': 'Symptom Checker',
        'diag-subtitle': 'Select symptoms or use voice input to get an AI-powered screening.',
        'history-title': 'Patient History', 'history-subtitle': 'View your previous diagnostic records.',
        'th-date': 'Date', 'th-symptoms': 'Symptoms', 'th-disease': 'Disease',
        'th-confidence': 'Confidence', 'loading': 'Loading...', 'no-history': 'No history found.',
        'nav-theme': 'Dark Mode', 'voice-lang-label': 'Voice Language:',
        'search-placeholder': 'Type to search or select symptoms manually...',
        'btn-diagnose': 'Diagnose', 'btn-clear': 'Clear', 'btn-refresh': 'Refresh',
        'explain-title': 'Disease Explanation',
        'explain-subtitle': 'Get detailed, easy-to-understand explanations.',
        'btn-download-report': 'Download Report',
        'q-yes': 'Yes', 'q-no': 'No', 'q-skip': 'Skip / Show Result',
        'res-diagnosis': 'Diagnosis', 'res-confidence': 'Confidence',
        'res-severity': 'Severity', 'res-specialist': 'Specialist',
        'res-emergency': 'Emergency?', 'res-emergency-yes': 'YES 🚨', 'res-emergency-no': 'No',
        'res-treatment': '💊 Recommended Treatment / Medications',
        'res-diet': '🍲 Diet Recommendations', 'res-lifestyle': '🏋️ Lifestyle & Workout',
        'res-precautions': '🛡️ Precautions', 'res-btn-explain': 'Explain Disease', 'res-btn-report': 'Get Report',
        'res-btn-doctor': 'Get Doctor Address', 'doc-loc-error': 'Location access denied or unavailable.', 'doc-finding': 'Finding Doctors nearby...',
        'doc-none': 'No specific doctors found nearby. Showing general physicians.', 'doc-contact': 'Contact', 'doc-exp': 'Exp'
    },
    'hi': {
        'app-name': 'स्वास्थ्यAI', 'logout': 'लॉगआउट', 'nav-diagnosis': 'निदान',
        'nav-explain': 'बीमारी स्पष्ट करें', 'nav-report': 'मेडिकल रिपोर्ट',
        'nav-image': 'छवि विश्लेषण', 'nav-dictionary': 'शब्दकोश',
        'nav-history': 'मरीज़ का इतिहास', 'diag-title': 'लक्षण जाँचकर्ता',
        'diag-subtitle': 'लक्षण चुनें या एआई-पावर्ड स्क्रीनिंग के लिए वॉयस इनपुट का उपयोग करें।',
        'history-title': 'मरीज़ का इतिहास', 'history-subtitle': 'अपने पिछले नैदानिक रिकॉर्ड देखें।',
        'th-date': 'तारीख', 'th-symptoms': 'लक्षण', 'th-disease': 'बीमारी',
        'th-confidence': 'विश्वास', 'loading': 'लोड हो रहा है...', 'no-history': 'कोई इतिहास नहीं मिला।',
        'nav-theme': 'डार्क मोड', 'voice-lang-label': 'आवाज की भाषा:',
        'search-placeholder': 'खोजने के लिए टाइप करें या मैन्युअल रूप से लक्षण चुनें...',
        'btn-diagnose': 'निदान करें', 'btn-clear': 'साफ करें', 'btn-refresh': 'ताज़ा करें',
        'explain-title': 'रोग स्पष्टीकरण',
        'explain-subtitle': 'विस्तृत, आसानी से समझ में आने वाले स्पष्टीकरण प्राप्त करें।',
        'btn-download-report': 'रिपोर्ट डाउनलोड करें',
        'q-yes': 'हाँ', 'q-no': 'नहीं', 'q-skip': 'छोड़ें / परिणाम दिखाएं',
        'res-diagnosis': 'निदान', 'res-confidence': 'विश्वास',
        'res-severity': 'गंभीरता', 'res-specialist': 'विशेषज्ञ',
        'res-emergency': 'आपातकालीन?', 'res-emergency-yes': 'हाँ 🚨', 'res-emergency-no': 'नहीं',
        'res-treatment': '💊 अनुशंसित उपचार / दवाएं',
        'res-diet': '🍲 आहार संबंधी सिफारिशें', 'res-lifestyle': '🏋️ जीवनशैली और कसरत',
        'res-precautions': '🛡️ सावधानियां', 'res-btn-explain': 'बीमारी स्पष्ट करें', 'res-btn-report': 'रिपोर्ट प्राप्त करें',
        'res-btn-doctor': 'डॉक्टर का पता प्राप्त करें', 'doc-loc-error': 'स्थान तक पहुंच अस्वीकृत।', 'doc-finding': 'नजदीकी डॉक्टर खोज रहे हैं...',
        'doc-none': 'आसपास कोई विशिष्ट डॉक्टर नहीं मिला।', 'doc-contact': 'संपर्क', 'doc-exp': 'अनुभव'
    },
    'gu': {
        'app-name': 'હેલ્થAI', 'logout': 'લોગઆઉટ', 'nav-diagnosis': 'નિદાન',
        'nav-explain': 'બીમારી સમજાવો', 'nav-report': 'મેડિકલ રિપોર્ટ',
        'nav-image': 'છબી વિશ્લેષણ', 'nav-dictionary': 'શબ્દકોશ',
        'nav-history': 'દર્દીનો ઇતિહાસ', 'diag-title': 'લક્ષણ તપાસનાર',
        'diag-subtitle': 'લક્ષણો પસંદ કરો અથવા AI-સંચાલિત સ્ક્રિનિંગ માટે વૉઇસ ઇનપુટનો ઉપયોગ કરો.',
        'history-title': 'દર્દીનો ઇતિહાસ', 'history-subtitle': 'તમારા પાછલા નિદાન રેકોર્ડ્સ જુઓ.',
        'th-date': 'તારીખ', 'th-symptoms': 'લક્ષણો', 'th-disease': 'બીમારી',
        'th-confidence': 'વિશ્વાસ', 'loading': 'લોડ થઈ રહ્યું છે...', 'no-history': 'કોઈ ઇતિહાસ મળ્યો નથી.',
        'nav-theme': 'ડાર્ક મોડ', 'voice-lang-label': 'વૉઇસ ભાષા:',
        'search-placeholder': 'શોધવા માટે લખો અથવા મેન્યુઅલી લક્ષણો પસંદ કરો...',
        'btn-diagnose': 'નિદાન કરો', 'btn-clear': 'સાફ કરો', 'btn-refresh': 'તાજું કરો',
        'explain-title': 'બીમારી સમજૂતી',
        'explain-subtitle': 'વિગતવાર અને સમજવામાં સરળ સમજૂતી મેળવો.',
        'btn-download-report': 'રિપોર્ટ ડાઉનલોડ કરો',
        'q-yes': 'હા', 'q-no': 'ના', 'q-skip': 'રદ કરો / પરિણામ બતાવો',
        'res-diagnosis': 'નિદાન', 'res-confidence': 'વિશ્વાસ',
        'res-severity': 'ગંભીરતા', 'res-specialist': 'નિષ્ણાત',
        'res-emergency': 'કટોકટી?', 'res-emergency-yes': 'હા 🚨', 'res-emergency-no': 'ના',
        'res-treatment': '💊 ભલામણ કરેલ સારવાર / દવાઓ',
        'res-diet': '🍲 આહાર ભલામણો', 'res-lifestyle': '🏋️ જીવનશૈલી અને કસરત',
        'res-precautions': '🛡️ સાવચેતીઓ', 'res-btn-explain': 'બીમારી સમજાવો', 'res-btn-report': 'રિપોર્ટ મેળવો',
        'res-btn-doctor': 'ડોક્ટરનું સરનામું મેળવો', 'doc-loc-error': 'લોકેશન એક્સેસ નથી.', 'doc-finding': 'નજીકના ડોક્ટર શોધી રહ્યા છીએ...',
        'doc-none': 'નજીકમાં કોઈ ચોક્કસ ડોક્ટર મળ્યા નથી.', 'doc-contact': 'સંપર્ક', 'doc-exp': 'અનુભવ'
    }
};

function changeLanguage(lang) {
    currentLang = lang;

    // Update Buttons UI
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(`'${lang}'`)) btn.classList.add('active');
    });

    // Translate all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (UI_STRINGS[lang][key]) {
            el.textContent = UI_STRINGS[lang][key];
        }
    });

    // Translate placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (UI_STRINGS[lang][key]) {
            el.placeholder = UI_STRINGS[lang][key];
        }
    });

    // Refresh Manual Dropdown
    renderSymptomDropdown();

    // Sync voice language dropdown
    const voiceSelect = document.getElementById('voice-lang');
    if (voiceSelect) {
        if (lang === 'hi') voiceSelect.value = 'hi-IN';
        else if (lang === 'gu') voiceSelect.value = 'gu-IN';
        else voiceSelect.value = 'en-IN';
    }
}

function renderSymptomDropdown() {
    const list = document.getElementById('symptom-list-manual');
    if (!list) return;
    list.innerHTML = '';

    ALL_SYMPTOMS.forEach(sym => {
        let displayName = sym;
        // Case-insensitive lookup in Map
        if (currentLang !== 'en' && SYMPTOM_MAP[currentLang]) {
            // Find key that matches sym (case-insensitive)
            const mapKeys = Object.keys(SYMPTOM_MAP[currentLang]);
            const matchKey = mapKeys.find(k => k.toLowerCase() === sym.toLowerCase());
            if (matchKey) {
                displayName = SYMPTOM_MAP[currentLang][matchKey];
            }
        }

        const opt = document.createElement('option');
        opt.value = displayName;
        opt.setAttribute('data-en', sym);
        list.appendChild(opt);
    });
}

// Helper for API calls with session handling
async function apiFetch(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (res.status === 401) {
            window.location.href = '/?error=Session expired';
            return null;
        }
        return res;
    } catch (e) {
        throw e;
    }
}

// --- TABS ---
function switchTab(tabId) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

    // Show selected
    document.getElementById(tabId).classList.add('active');

    // Update nav
    const navBtn = Array.from(document.querySelectorAll('.nav-item')).find(el => el.textContent.toLowerCase().includes(tabId));
    if (navBtn) navBtn.classList.add('active');

    // Special load for dictionary
    if (tabId === 'dictionary') loadDictionary();
    if (tabId === 'history') loadUserHistory();
}

// --- SYMPTOM INPUT ---
const searchInput = document.getElementById('symptom-search');
const suggestionsList = document.getElementById('symptom-suggestions');
const selectedList = document.getElementById('selected-list');

searchInput.addEventListener('input', (e) => {
    const query = e.target.value;

    // 1. Check if input matches a LOCALIZED symptom name (datalist selection)
    let englishMatch = null;
    if (ALL_SYMPTOMS.includes(query)) {
        englishMatch = query;
    } else {
        // Look for the English original in SYMPTOM_MAP
        if (currentLang !== 'en' && SYMPTOM_MAP[currentLang]) {
            for (const [en, local] of Object.entries(SYMPTOM_MAP[currentLang])) {
                if (local === query) { englishMatch = en; break; }
            }
        }
    }

    if (englishMatch) {
        addSymptom(englishMatch);
        e.target.value = "";
        return;
    }

    const queryLower = query.toLowerCase().trim();
    suggestionsList.innerHTML = '';

    if (queryLower.length < 2) {
        suggestionsList.classList.add('hidden');
        return;
    }

    // Prepare a list of display names and their English counterparts
    const searchPool = ALL_SYMPTOMS.map(en => {
        let display = en;
        if (currentLang !== 'en' && SYMPTOM_MAP[currentLang]) {
            const mapKeys = Object.keys(SYMPTOM_MAP[currentLang]);
            const matchKey = mapKeys.find(k => k.toLowerCase() === en.toLowerCase());
            if (matchKey) {
                display = SYMPTOM_MAP[currentLang][matchKey];
            }
        }
        return { en, display };
    });

    const matches = searchPool.filter(item =>
        (item.display.toLowerCase().includes(queryLower) || item.en.toLowerCase().includes(queryLower))
        && !selectedSymptoms.includes(item.en)
    );

    if (matches.length > 0) {
        suggestionsList.classList.remove('hidden');
        matches.slice(0, 10).forEach(match => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            div.innerHTML = `<span>${match.display}</span>${currentLang !== 'en' ? `<small style="display:block; font-size: 0.7rem; color: var(--text-muted);">${match.en}</small>` : ''}`;
            div.onclick = () => addSymptom(match.en);
            suggestionsList.appendChild(div);
        });
    } else {
        suggestionsList.classList.add('hidden');
    }
});

function addSymptom(symptom) {
    if (selectedSymptoms.includes(symptom)) return;

    selectedSymptoms.push(symptom);
    renderChips();
    searchInput.value = '';
    suggestionsList.classList.add('hidden');
}

function removeSymptom(symptom) {
    selectedSymptoms = selectedSymptoms.filter(s => s !== symptom);
    renderChips();
}

function clearSymptoms() {
    selectedSymptoms = [];
    askedSymptoms = [];
    renderChips();
    document.getElementById('interaction-area').classList.add('hidden');
    document.getElementById('interaction-area').innerHTML = "";
    document.getElementById('symptom-search').value = "";
    document.getElementById('spoken-text-display').classList.add('hidden');
    document.getElementById('spoken-text-display').innerHTML = "";
}

function renderChips() {
    selectedList.innerHTML = '';
    selectedSymptoms.forEach(s => {
        let label = s;
        if (currentLang !== 'en' && SYMPTOM_MAP[currentLang] && SYMPTOM_MAP[currentLang][s]) {
            label = SYMPTOM_MAP[currentLang][s];
        }
        const chip = document.createElement('div');
        chip.className = 'chip';
        chip.innerHTML = `${label} <i class="fa-solid fa-xmark" onclick="removeSymptom('${s}')"></i>`;
        selectedList.appendChild(chip);
    });
}

// --- VOICE INPUT ---
// --- THEME TOGGLE ---
const themeToggleBtn = document.getElementById('theme-toggle');
if (themeToggleBtn) {
    themeToggleBtn.onclick = () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        const btnText = isDark ? UI_STRINGS[currentLang]['nav-theme-light'] || 'Light Mode' : UI_STRINGS[currentLang]['nav-theme'] || 'Dark Mode';
        themeToggleBtn.innerHTML = `<i class="fa-solid fa-${isDark ? 'sun' : 'moon'}"></i> ${btnText}`;
    };
}

// --- VOICE INPUT ---
const voiceBtn = document.getElementById('voice-btn');
const voiceLangSelect = document.getElementById('voice-lang');
const spokenTextDisplay = document.getElementById('spoken-text-display');

voiceBtn.onclick = () => {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Voice input not supported in this browser. Try Chrome.");
        return;
    }

    // Get selected language code
    const langCode = voiceLangSelect ? voiceLangSelect.value : 'en-IN';

    const recognition = new webkitSpeechRecognition();
    recognition.lang = langCode;
    recognition.start();

    voiceBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    spokenTextDisplay.innerHTML = '<i>Listening...</i>';
    spokenTextDisplay.classList.remove('hidden');

    recognition.onresult = async (event) => {
        const text = event.results[0][0].transcript;
        console.log("Recorded:", text);

        // Display Text
        spokenTextDisplay.innerHTML = `<strong>You said:</strong> "${text}"<br/><span style="color: var(--primary); font-size: 0.85rem;"><i class="fa-solid fa-spinner fa-spin"></i> Detecting symptoms...</span>`;

        // Send to backend for extraction
        try {
            const res = await apiFetch('/api/extract_symptoms', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text, language: langCode })
            });
            if (!res) return;
            const data = await res.json();

            if (data.status === 'success') {
                spokenTextDisplay.innerHTML = `<strong>You said:</strong> "${text}"`;
                if (data.symptoms.length > 0) {
                    data.symptoms.forEach(s => addSymptom(s));
                    // alert(`Detected: ${data.symptoms.join(", ")}`); // Removed alert, UI is enough
                } else {
                    spokenTextDisplay.innerHTML += `<br><span class="text-error">No symptoms detected. Try simpler words.</span>`;
                }
            } else {
                spokenTextDisplay.innerHTML += `<br><span class="text-error">Detection failed.</span>`;
            }
        } catch (e) {
            console.error(e);
            spokenTextDisplay.innerHTML += `<br><span class="text-error">Error: ${e.message}</span>`;
        }

        voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
    };

    recognition.onerror = () => {
        voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
        spokenTextDisplay.innerHTML = '<span style="color:red">Voice recognition error. Check microphone permissions.</span>';
    };
};

// --- DIAGNOSIS LOGIC ---
async function startDiagnosis(forceFinal = false) {
    if (selectedSymptoms.length === 0) {
        alert("Please select at least one symptom.");
        return;
    }

    const interactionArea = document.getElementById('interaction-area');
    interactionArea.classList.remove('hidden');
    interactionArea.innerHTML = '<p><i class="fa-solid fa-spinner fa-spin"></i> Analyzing...</p>';

    try {
        const voiceLang = document.getElementById('voice-lang').value;
        const res = await apiFetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symptoms: selectedSymptoms,
                asked_symptoms: askedSymptoms,
                force_final: forceFinal,
                language: voiceLang
            })
        });

        if (!res) return;
        const data = await res.json();

        if (data.status === 'question') {
            const qText = data.question_text || `Do you also experience <strong>${data.question_symptom}</strong>?`;
            renderQuestion(data.question_symptom, qText);
        } else if (data.status === 'final') {
            renderResult(data.result);
        }

    } catch (e) {
        interactionArea.innerHTML = `<p class="text-red-500">Error: ${e.message}</p>`;
    }
}

function renderQuestion(symptom, text) {
    const area = document.getElementById('interaction-area');
    // If text doesn't contain HTML tags, wrap it? The backup text has <strong>, but localized might not.
    // Let's trust the backend or the fallback.
    area.innerHTML = `
        <h3>${text}</h3>
        <div class="action-buttons" style="justify-content: center; margin-top: 1rem;">
            <button class="btn btn-primary" onclick="answerQuestion('${symptom}', true)">${UI_STRINGS[currentLang]['q-yes'] || 'Yes'}</button>
            <button class="btn btn-secondary" onclick="answerQuestion('${symptom}', false)">${UI_STRINGS[currentLang]['q-no'] || 'No'}</button>
            <button class="btn btn-accent" onclick="startDiagnosis(true)">${UI_STRINGS[currentLang]['q-skip'] || 'Skip / Show Result'}</button>
        </div>
    `;
}

function answerQuestion(symptom, isYes) {
    askedSymptoms.push(symptom);
    if (isYes) {
        selectedSymptoms.push(symptom);
        renderChips();
    }
    startDiagnosis();
}

function renderResult(result) {
    const area = document.getElementById('interaction-area');
    const info = result.info;

    area.innerHTML = `
        <h2 style="color: var(--primary-dark)">${UI_STRINGS[currentLang]['res-diagnosis'] || 'Diagnosis'}: ${result.disease}</h2>
        <p style="color: var(--text-muted); margin-bottom: 1rem;">${UI_STRINGS[currentLang]['res-confidence'] || 'Confidence'}: ${(result.confidence * 100).toFixed(1)}%</p>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;">
             <div class="message-card">
                <strong>${UI_STRINGS[currentLang]['res-severity'] || 'Severity'}</strong><br>${info.severity}
             </div>
             <div class="message-card">
                <strong>${UI_STRINGS[currentLang]['res-specialist'] || 'Specialist'}</strong><br>${info.specialist}
             </div>
             <div class="message-card ${info.emergency ? 'warning' : ''}">
                <strong>${UI_STRINGS[currentLang]['res-emergency'] || 'Emergency?'}</strong><br>${info.emergency ? UI_STRINGS[currentLang]['res-emergency-yes'] : UI_STRINGS[currentLang]['res-emergency-no']}
             </div>
        </div>
        
        <div class="message-card">
            <strong>${UI_STRINGS[currentLang]['res-treatment'] || '💊 Recommended Treatment / Medications'}</strong>
            ${info.medications && info.medications.length > 0 ? `
                <ul style="margin-top: 0.5rem; padding-left: 1.2rem;">
                    ${info.medications.map(m => `<li>${m}</li>`).join('')}
                </ul>
            ` : `<p>${info.treatment || 'Consult a doctor for specific medications.'}</p>`}
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            ${info.diets && info.diets.length > 0 ? `
                <div class="message-card" style="border-left: 4px solid #10b981;">
                    <strong>${UI_STRINGS[currentLang]['res-diet'] || '🍲 Diet Recommendations'}</strong>
                    <ul style="margin-top: 0.5rem; padding-left: 1.2rem; font-size: 0.9rem;">
                        ${info.diets.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${info.workouts && info.workouts.length > 0 ? `
                <div class="message-card" style="border-left: 4px solid #3b82f6;">
                    <strong>${UI_STRINGS[currentLang]['res-lifestyle'] || '🏋️ Lifestyle & Workout'}</strong>
                    <ul style="margin-top: 0.5rem; padding-left: 1.2rem; font-size: 0.9rem;">
                        ${info.workouts.map(w => `<li>${w}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
        
        ${info.precautions && info.precautions.length > 0 ? `
            <div class="message-card warning" style="margin-top: 1rem;">
                <strong>${UI_STRINGS[currentLang]['res-precautions'] || '🛡️ Precautions'}</strong>
                <ul style="margin-top: 0.5rem; padding-left: 1.2rem;">
                    ${info.precautions.map(p => `<li>${p}</li>`).join('')}
                </ul>
            </div>
        ` : ''}

        <div style="display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;">
            <button class="btn btn-primary" style="flex: 1; min-width: 120px;" onclick="window.scrollTo(0,0); switchTab('explain');">
                <i class="fa-solid fa-book-medical"></i> ${UI_STRINGS[currentLang]['res-btn-explain'] || 'Explain'}
            </button>
            <button class="btn btn-secondary" style="flex: 1; min-width: 120px;" onclick="window.scrollTo(0,0); switchTab('report');">
                <i class="fa-solid fa-file-pdf"></i> ${UI_STRINGS[currentLang]['res-btn-report'] || 'Report'}
            </button>
            <button class="btn" style="flex: 1; min-width: 120px; background-color: #8b5cf6; color: white;" onclick="getDoctorAddress('${result.disease.replace(/'/g, "\\'")}')">
                <i class="fa-solid fa-user-doctor"></i> ${UI_STRINGS[currentLang]['res-btn-doctor'] || 'Doctor'}
            </button>
        </div>
        
        <div id="doctor-results-area" class="hidden" style="margin-top: 1.5rem; border-top: 1px dashed var(--border-color); padding-top: 1rem;"></div>
    `;

    // Auto-fill other tabs
    document.getElementById('explain-disease-input').value = result.disease;
    document.getElementById('report-disease-input').value = result.disease;
}

// --- OTHER TABS ---

// Explain
async function explainDisease(lang) {
    const disease = document.getElementById('explain-disease-input').value;
    const resContainer = document.getElementById('explain-result-container');
    const resBox = document.getElementById('explain-result');

    if (!disease) return alert("Enter disease name");

    resContainer.classList.remove('hidden');
    resBox.textContent = "Generating explanation...";

    const res = await apiFetch('/api/explain_disease', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disease, language: lang })
    });
    if (!res) return;
    const data = await res.json();


    // Format the text for better display
    if (data.explanation) {
        let text = data.explanation;

        // 1. Convert **Bold** to <strong>Bold</strong>
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // 2. Handle numbered lists better (ensure they start on new lines)
        // Look for patterns like "1. TITLE:" and ensure a break before them
        text = text.replace(/(\d+\.\s+[A-Z\s]+:)/g, '<br><br>$1');

        // 3. Convert remaining newlines to <br>
        text = text.replace(/\n/g, '<br>');

        // 4. Clean up initial double breaks if any
        if (text.startsWith('<br>')) text = text.substring(4);

        resBox.innerHTML = text;
    } else {
        resBox.textContent = data.error;
    }
}

// Report
function selectReportLang(lang) {
    reportLang = lang;
    document.querySelectorAll('.lang-rpt-btn').forEach(btn => btn.classList.remove('active'));
    // Map lang to button IDs
    const idMap = { 'English': 'rpt-en', 'Hindi': 'rpt-hi', 'Gujarati': 'rpt-gu' };
    document.getElementById(idMap[lang]).classList.add('active');
}

async function generateReport() {
    const disease = document.getElementById('report-disease-input').value;
    if (!disease) return alert("Enter disease name");

    const btn = document.querySelector('[onclick="generateReport()"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';
    btn.disabled = true;

    try {
        const res = await fetch('/api/generate_report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ disease, language: reportLang })
        });

        if (res.status === 401) {
            window.location.href = '/?error=Session expired';
            return;
        }

        if (!res.ok) throw new Error("Server error");

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Medical_Report_${disease}_${reportLang}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (err) {
        alert("Error generating report: " + err.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Image
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('image-upload');
const preview = document.getElementById('image-preview');

dropZone.onclick = () => fileInput.click();

fileInput.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
        preview.src = URL.createObjectURL(file);
        document.getElementById('image-preview-area').classList.remove('hidden');
        dropZone.classList.add('hidden');
    }
};

async function analyzeImage() {
    const file = fileInput.files[0];
    if (!file) return alert("Upload an image first");

    const resBox = document.getElementById('image-result');
    resBox.classList.remove('hidden');
    resBox.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

    const formData = new FormData();
    formData.append('image', file);

    const res = await apiFetch('/api/analyze_image', {
        method: 'POST',
        body: formData
    });
    if (!res) return;
    const data = await res.json();
    resBox.textContent = data.result || data.error;
}

// Dictionary
let dictData = [];
async function loadDictionary() {
    if (dictData.length > 0) return;

    const body = document.getElementById('dict-body');
    body.innerHTML = '<tr><td colspan="3">Loading dictionary...</td></tr>';

    const res = await apiFetch('/api/dictionary');
    if (!res) return;
    const data = await res.json();
    dictData = data.terms; // Array of objects {en, hi, gu}
    renderDictionary(dictData);
}

function renderDictionary(data) {
    const body = document.getElementById('dict-body');
    body.innerHTML = '';

    // Limit to 100 for performance initially
    data.slice(0, 100).forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${item.en}</td><td>${item.hi}</td><td>${item.gu}</td>`;
        body.appendChild(tr);
    });
}

function filterDictionary() {
    const term = document.getElementById('dict-search').value.toLowerCase();
    const filtered = dictData.filter(item =>
        item.en.includes(term) || item.hi.includes(term) || item.gu.includes(term)
    );
    renderDictionary(filtered);
}

// History
async function loadUserHistory() {
    const body = document.getElementById('history-body');
    body.innerHTML = '<tr><td colspan="4"><i class="fa-solid fa-spinner fa-spin"></i> Loading...</td></tr>';

    try {
        const res = await apiFetch('/api/user_history');
        if (!res) return;
        const data = await res.json();

        if (data.status === 'success') {
            if (data.history.length === 0) {
                body.innerHTML = '<tr><td colspan="4">No history found.</td></tr>';
                return;
            }

            body.innerHTML = '';
            data.history.forEach(h => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${h.timestamp}</td>
                    <td><small>${h.symptoms.join(", ")}</small></td>
                    <td><strong>${h.disease}</strong></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div style="width: 50px; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                                <div style="width: ${h.confidence}%; height: 100%; background: var(--primary-color);"></div>
                            </div>
                            <span>${h.confidence}%</span>
                        </div>
                    </td>
                `;
                body.appendChild(tr);
            });
        }
    } catch (e) {
        body.innerHTML = `<tr><td colspan="4" class="text-error">Error: ${e.message}</td></tr>`;
    }
}

// --- DOCTOR FINDER ---
function getDoctorAddress(disease) {
    const area = document.getElementById('doctor-results-area');
    area.classList.remove('hidden');
    area.innerHTML = `<p><i class="fa-solid fa-spinner fa-spin"></i> ${UI_STRINGS[currentLang]['doc-finding'] || 'Finding Doctors...'}</p>`;

    if (!navigator.geolocation) {
        area.innerHTML = `<p class="text-error">${UI_STRINGS[currentLang]['doc-loc-error'] || 'Geolocation not supported.'}</p>`;
        return;
    }

    navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;

        try {
            const res = await apiFetch('/api/find_doctors', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat: latitude, lng: longitude, disease: disease })
            });

            if (!res) return;
            const data = await res.json();

            if (data.doctors && data.doctors.length > 0) {
                let html = `<h3 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--primary-dark);">
                    <i class="fa-solid fa-location-dot"></i> Doctors in ${data.city_detected} (${data.specialist_required})
                </h3>`;

                html += `<div style="display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));">`;

                data.doctors.forEach(doc => {
                    html += `
                        <div class="card" style="padding: 1rem; border: 1px solid var(--border-color); box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <div style="display:flex; justify-content:space-between; align-items:start;">
                                <h4 style="color: var(--primary); margin-bottom: 0.5rem;">${doc.doctor_name}</h4>
                                <span style="background: #e0f2fe; color: #0284c7; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">${doc.experience_years}</span>
                            </div>
                            <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.5rem;">
                                ${doc.qualification} | ${doc.specialization}
                            </p>
                            <p style="font-size: 0.85rem; margin-bottom: 0.5rem;">
                                <i class="fa-solid fa-map-pin"></i> ${doc.service_areas}
                            </p>
                            <div style="display: flex; gap: 0.5rem; margin-top: 0.8rem;">
                                <a href="tel:${doc.phone_number}" class="btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">
                                    <i class="fa-solid fa-phone"></i> Call
                                </a>
                                <a href="https://wa.me/${doc.whatsapp_number}" target="_blank" class="btn" style="background: #25D366; color: white; padding: 0.4rem 0.8rem; font-size: 0.85rem;">
                                    <i class="fa-brands fa-whatsapp"></i> WhatsApp
                                </a>
                            </div>
                        </div>
                    `;
                });

                html += `</div>`;
                area.innerHTML = html;
            } else {
                area.innerHTML = `<p>${UI_STRINGS[currentLang]['doc-none'] || 'No nearby doctors found.'}</p>`;
            }

        } catch (e) {
            area.innerHTML = `<p class="text-error">Error: ${e.message}</p>`;
        }
    }, (err) => {
        console.error(err);
        area.innerHTML = `<p class="text-error">${UI_STRINGS[currentLang]['doc-loc-error']} (Code: ${err.code})</p>`;
    });
}