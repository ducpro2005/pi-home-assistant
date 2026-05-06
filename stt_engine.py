import json
import os
import wave
import time
from vosk import Model, KaldiRecognizer

MODEL_PATH = "model" 
SAMPLE_RATE = 16000

ALLOWED_WORDS = [
    "can", "could", "would", "will", "you", "please", 
    "for", "me", "hey", "hi", "hello", "okay", "ok", "thanks",  
    "a", "an", "the", "my", "some", "it", "that", "this", "is", "in", "to", "at",
    "turn", "switch", "power", "set", "make", "open", "close", "lock", "unlock", "start", "stop",
    "on", "off", "up", "down", "high", "low", "medium",
    "light", "lights", "lamp", "fan", "ac", "air", "conditioner", "door", "heater", "tv", "television", "speaker", "blinds",
    
    "kitchen", "bedroom", "living", "room", "bathroom", "garage", "front", "back", "hallway", "office", "floor", "three",
    "[unk]"
]
GRAMMAR_JSON = json.dumps(ALLOWED_WORDS)

print("[STT Engine] Booting up... Loading Vosk model into memory.")
if not os.path.exists(MODEL_PATH):
    print(f"[STT Error] Could not find the model folder.")
    vosk_model = None
else:
    vosk_model = Model(MODEL_PATH) 
    print("[STT Engine] Model loaded successfully.")

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Takes a raw 16kHz, 16-bit, mono audio byte array.
    Returns the transcribed text string.
    """
    if not vosk_model or not audio_bytes:
        return ""

    # Pass the strict grammar list into the Recognizer
    rec = KaldiRecognizer(vosk_model, SAMPLE_RATE, GRAMMAR_JSON)
    
    chunk_size = 4000
    for i in range(0, len(audio_bytes), chunk_size):
        chunk = audio_bytes[i:i + chunk_size]
        rec.AcceptWaveform(chunk)
    
    result_json = json.loads(rec.FinalResult())
    spoken_text = result_json.get("text", "")
    
    return spoken_text

if __name__ == "__main__":
    print("\n--- Testing Optimized STT Engine ---")
    
    test_audio_file = "test_recording.wav"
    
    if not os.path.exists(test_audio_file):
        print(f"Error: Need '{test_audio_file}' to run.")
    else:
        with wave.open(test_audio_file, "rb") as wf:
            raw_audio_bytes = wf.readframes(wf.getnframes())
            
        print("Feeding audio to Vosk (Grammar Restricted)...")
        
        start_time = time.time()
        transcription = transcribe_audio(raw_audio_bytes)
        end_time = time.time()
        
        print("\n==============================")
        print(f"You said: '{transcription}'")
        print(f"True Processing Time: {end_time - start_time:.2f} seconds")
        print("==============================\n")