# pipeline.py

import subprocess

# Run ASR
subprocess.call(["python", "asr2.py"])

# Translate to English
subprocess.call(["python", "translate.py"])

# Translate back to the original language
subprocess.call(["python", "translate.py"])

# Generate TTS
subprocess.call(["python", "tts2.py"])