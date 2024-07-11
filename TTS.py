from gtts import gTTS
import os
from pydub import AudioSegment
import platform

# Text to be spoken in Hindi
text = "नमस्ते! कैसे हो आप?"

# Specify the language (Hindi in this case)
language = 'hi'

# Create a gTTS object
tts = gTTS(text, lang=language, slow=False)

# Save the audio file
tts.save("output.mp3")

# Play the audio using a media player
os.system("start output.mp3")  # For Linux
# os.system("start output.mp3")  # For Windows

audio = AudioSegment.from_mp3("output.mp3")

# Play the audio
audio.play()