import sys
import codecs

if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

def test_matching():
    text = "mane mathu dukhe che"
    text_lower = text.lower().strip()
    
    STOPWORDS = {
        "mane", "k", "ke", "ane", "chhe", "che", "ma", "hu", "thay", "lage", 
        "jevu", "ave", "mate", "thi", "no", "ni", "nu", "na", "pan", "chho",
        "mujhe", "hai", "ho", "raha", "rahi", "ko", "me", "se", "aur", "ki", "ka",
        "dukhe", "dukhavo", "dukh", "aave", "lagu", "thavu",
        # Gujarati Script Stops
        "મને", "કે", "અને", "છે", "મા", "હું", "થાય", "લાગે", "જેવું", "આવે",
        "માટે", "થી", "નો", "ની", "નું", "ના", "પણ", "દુખે", "દુખાવો", "દુખ",
        "થવું", "આવવું", "લાગવું",
        # Hindi Script Stops (Added)
        "दर्द", "है", "का", "की", "के", "को", "में", "से", "और", "मुझे", "हो", "रहा", "रही", "हूं",
        "सूजन", "लगना", "आना" 
    }

    print("\n--- Testing Gothan (Knee Pain) ---")
    text_gothan = "મને ગોઠણ દુખે છે"
    key_gothan = "ગોઠણ દુખે"
    
    print(f"Input: {text_gothan}")
    print(f"Key: {key_gothan}")
    
    key_tokens = key_gothan.split()
    meaningful = [t for t in key_tokens if t not in STOPWORDS and len(t) >= 1]
    print(f"Key Tokens: {key_tokens}")
    print(f"Meaningful Tokens: {meaningful}")
    
    matches = 0
    for t in meaningful:
        if t in text_gothan:
            print(f"Match: {t}")
            matches += 1
            
    if not meaningful:
        print("No meaningful tokens.")
    else:
        ratio = matches / len(meaningful)
        print(f"Ratio: {ratio}")
        if matches >= 1 and (len(meaningful) == 1 or ratio >= 0.5):
            print("RESULT: MATCH FOUND (Success)")
        else:
            print("RESULT: NO MATCH (Fail)")

    # Check "Mathu dukhe" (Headache)
    key2 = "માથું દુખવું" # headache (from JSON line 271) - Wait, line 271 says "માથું દુખવું"
    # User said "mathu dukhe"
    # "mathu" vs "માથું" (Anusvara?)
    
    # Try to match headache too
    print("\n--- Testing Headache ---")
    key_tokens2 = key2.split()
    meaningful2 = [t for t in key_tokens2 if t not in STOPWORDS and len(t) >= 3]
    print(f"Headache Tokens: {meaningful2}")
    for t in meaningful2:
        if t in text_lower:
             print(f"Headache Match: {t}")

if __name__ == "__main__":
    test_matching()
