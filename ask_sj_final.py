import os
import subprocess
import json
import urllib.request
import time
from groq import Groq
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# --- CONFIGURATION ---
GROQ_API_KEY = "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"
DEEPGRAM_API_KEY = "216dd82d28fd746da52451efcf1f39826150d9df"

groq_client = Groq(api_key=GROQ_API_KEY)
AUDIO_OUTPUT = "response.wav"

SYSTEM_PROMPT = """
You are 'AskSJ', a warm mentor for Laksh at St. Joseph's. 
- Tone: Supportive. Start with "Hey Laksh".
- Context: GPA 8.7, VLSI Attendance 78%. 
- Responses: 2 sentences max. No emojis.
"""

# --- UTILITY FUNCTIONS ---
def check_internet():
    try:
        # Pings Google to check if the Pi has real internet
        urllib.request.urlopen('https://google.com', timeout=2)
        return True
    except:
        return False

def update_face(state):
    try:
        with open("status.txt", "w") as f:
            f.write(state)
    except:
        pass

# --- THE AI BRAIN & INTERCEPTORS ---
def get_ai_response(user_text):
    print(f"\nUSER: {user_text}")
    update_face("THINKING") 
    
    text_lower = user_text.lower()

    # 1. 🎓 THE PRACTICE ARENA TRAP
    if "practice" in text_lower or "test" in text_lower or "mcq" in text_lower:
        return {
            "text": "Initializing the Practice Arena. Let's sharpen those skills, Laksh.",
            "action": "test_mode" 
        }

    # 2. 🔥 THE DEEP WORK TRAP
    if "focus" in text_lower or "deep work" in text_lower or "study" in text_lower:
        os.system("xdg-open 'https://open.spotify.com/search/seedhe%20maut' > /dev/null 2>&1 &") 
        return {
            "text": "Activating Deep Work Protocol. 25-minute Pomodoro timer engaged. Firing up the focus playlist. Let's get to work.",
            "action": "focus_mode" 
        }

    # 3. 🛡️ THE FATIGUE GUARDIAN TRAP
    if "weather" in text_lower:
        try:
            req = urllib.request.Request("https://wttr.in/?format=j1", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())
                temp = data['current_condition'][0]['temp_C']
                desc = data['current_condition'][0]['weatherDesc'][0]['value'].lower()
                loc = data['nearest_area'][0]['areaName'][0]['value']
                return {"text": f"It's currently {temp} degrees and {desc} in {loc}. Step away from the screen and rest those eyes.", "action": "none"}
        except Exception:
            return {"text": "It's around 32 degrees outside. Make sure you step away from the screen and rest your eyes, Laksh.", "action": "none"}
        
    # 4. 🎵 THE MUSIC TRAP
    if "play music" in text_lower or "spotify" in text_lower:
        os.system("xdg-open 'https://open.spotify.com/search/seedhe%20maut' > /dev/null 2>&1 &") 
        return {"text": "Firing up some Seedhe Maut. Let's get this project across the finish line.", "action": "none"}
    
    # 5. 🧠 DYNAMIC BRAIN FAILOVER (GROQ vs OLLAMA)
    if check_internet():
        print("[NETWORK] Online. Using Groq.")
        try:
            completion = groq_client.chat.completions.create(
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_text}],
                model="llama-3.1-8b-instant",
            )
            return {"text": completion.choices[0].message.content, "action": "none"}
        except Exception as e:
            return {"text": f"Groq API Error: {e}", "action": "none"}
    else:
        print("[NETWORK] Offline. Submarine Mode Engaged (TinyLlama).")
        try:
            result = subprocess.run(
                ['ollama', 'run', 'tinyllama', f"You are AskSJ, a mentor. Answer briefly: {user_text}"], 
                capture_output=True, text=True
            )
            return {"text": result.stdout.strip(), "action": "none"}
        except Exception as e:
            return {"text": "Critical Error. Local neural core offline.", "action": "none"}

# --- THE VOICE ENGINE ---
def speak_with_emotion(text):
    print(f"ASKSJ: {text}")
    
    # OFFLINE VOICE: eSpeak
    if not check_internet():
        print("[NETWORK] Offline Voice: Using eSpeak")
        update_face("SPEAKING") 
        subprocess.run(["espeak", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    # ONLINE VOICE: Deepgram
    print("[NETWORK] Online Voice: Using Deepgram")
    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en&encoding=linear16&container=wav"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps({"text": text}).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(AUDIO_OUTPUT, 'wb') as f:
                f.write(response.read())
        
        update_face("SPEAKING") 
        subprocess.run(["pw-play", AUDIO_OUTPUT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except Exception as e:
        print(f"❌ Voice Error: {e}")
        # Fallback to espeak if Deepgram crashes
        subprocess.run(["espeak", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --- WEB SERVER ROUTES ---
@app.route('/')
def serve_ui():
    return send_file('index.html')

@app.route('/status.txt')
def serve_status():
    return send_file('status.txt')

@app.route('/ask', methods=['POST'])
def ask():
    user_text = request.json.get('question')
    if user_text:
        ai_data = get_ai_response(user_text)
        speak_with_emotion(ai_data["text"])
        update_face("IDLE")
        return jsonify({"success": True, "answer": ai_data["text"], "action": ai_data["action"]})
    return jsonify({"error": "No text"})

@app.route('/voice', methods=['POST'])
def voice():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"})
    
    request.files['audio'].save("temp_voice.webm")
    update_face("THINKING")
    
    # Whisper Voice-to-Text requires internet!
    if not check_internet():
        update_face("IDLE")
        return jsonify({"success": False, "error": "Voice transcription requires internet. Please type your command."})

    try:
        with open("temp_voice.webm", "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
              file=("temp_voice.webm", file.read()),
              model="whisper-large-v3",
            )
        
        user_text = transcription.text.strip()
        if not user_text:
            return jsonify({"success": False})

        ai_data = get_ai_response(user_text)
        speak_with_emotion(ai_data["text"])
        update_face("IDLE")
        
        return jsonify({"success": True, "text": user_text, "answer": ai_data["text"], "action": ai_data["action"]})
        
    except Exception as e:
        print(f"Whisper Error: {e}")
        update_face("IDLE")
        return jsonify({"success": False})

if __name__ == "__main__":
    print("AskSJ Intercom Online - Waiting for Web UI...")
    update_face("IDLE")
    # Suppress Flask default logging for a cleaner terminal
    import logging
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='0.0.0.0', port=8000)
