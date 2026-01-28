 zimport speech_recognition as sr
import pyaudio
import openai

print("SpeechRecognition version:", sr.__version__)
print("PyAudio imported successfully")
print("OpenAI imported successfully")
try:
    p = pyaudio.PyAudio()
    print("PyAudio initialized successfully with default host api count:", p.get_host_api_count())
    p.terminate()
except Exception as e:
    print("PyAudio initialization failed:", e)
