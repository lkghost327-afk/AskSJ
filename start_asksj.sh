#!/bin/bash
cd ~/intercom_project || exit

echo "[SYSTEM] Initiating Pre-Flight Memory Purge..."

# 1. THE RAM CLEARING PROTOCOL
# This forcefully closes heavy background apps before AskSJ starts
killall -9 chromium-browser 2>/dev/null
killall -9 chromium 2>/dev/null
killall -9 code 2>/dev/null
killall -9 vlc 2>/dev/null
killall -9 thunar 2>/dev/null

echo "[SYSTEM] RAM Cleared. Booting AskSJ Neural Core..."

# 2. Start the Flask server
python3 ask_sj_final.py &
PYTHON_PID=$!

echo "[SYSTEM] Warming up local servers... standby."
sleep 4  # Giving the Pi a slightly longer buffer to recover from the purge

# 3. Open a fresh, single UI window
xdg-open http://localhost:8000

# 4. Wait here so the terminal window stays open
wait $PYTHON_PID
