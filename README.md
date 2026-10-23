# AskSJ - Neural Guardian Intercom 🛡️

AskSJ is a multi-modal, context-aware AI desktop assistant designed for the Raspberry Pi 4. Built for the Cyber Knight Hackathon, it acts as a smart campus mentor with automatic internet-failover capabilities.

### ⚡ Key Features
* **Submarine Mode (Auto-Failover):** Uses Groq (LLaMA 3.1) and Deepgram for lightning-fast cloud responses. If Wi-Fi drops, it seamlessly routes to a local Ollama (TinyLlama) model and eSpeak TTS.
* **The Practice Arena:** A built-in, voice-triggered MCQ testing overlay with live scoring and a customizable timer.
* **Deep Work Protocol:** Voice-activated focus mode that locks the UI into an orange hue, starts a 25-minute Pomodoro timer, and launches a focus playlist via Spotify.
* **Fatigue Guardian:** Context-aware break reminders based on local weather conditions.
* **RAM-Optimized Launch:** Custom shell scripts execute a tactical memory sweep to clear background tasks before booting the Flask server.

### 🛠️ Tech Stack
* **Hardware:** Raspberry Pi 4 (2GB)
* **Backend:** Python, Flask, Subprocess threading
* **AI Core:** Groq API (LLaMA 3.1, Whisper), Ollama (Local LLM)
* **Voice Engine:** Deepgram Aura, eSpeak
* **Frontend:** HTML, CSS, JavaScript (Dynamic UI State Management)
