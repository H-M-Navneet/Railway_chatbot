import speech_recognition as sr

import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use a microphone as the audio source
with sr.Microphone() as source:
    print("ಏನು ಹೇಳಿ...")
    
    # Adjust for ambient noise
    recognizer.adjust_for_ambient_noise(source)
    
    # Listen to the user's speech
    audio = recognizer.listen(source)

    print("ಪ್ರಕ್ರಿಯಿಸಲಾಗುತ್ತಿದೆ...")

try:
    # Recognize speech in Kannada
    text = recognizer.recognize_google(audio, language="en")

    # Print the recognized text
    print("ನೀವು ಹೇಳಿದ್ದೀರಿ:", text)

except sr.UnknownValueError:
    print("ಕ್ಷಮಿಸಿ, ಆಡಿಯೋವನ್ನು ಗ್ರಹಿಸಲಾಗಲಿಲ್ಲ.")

except sr.RequestError as e:
    print(f"ಫಲಿತಾಂಶಗಳನ್ನು ವಿನಂತಿಸಲಾಗಲಿಲ್ಲ; {e}")
