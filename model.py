import requests
import speech_recognition as sr
import pyttsx3
import googletrans
from googletrans import Translator

# API endpoint URLs
UPLOAD_URL = 'http://your_server_url/upload'
GET_AUDIO_URL = 'http://your_server_url/get_audio/'

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
trans = Translator()

# Function to recognize and translate audio
def recognize_and_translate(audio_id):
    audio_url = GET_AUDIO_URL + audio_id

    with sr.AudioFile(audio_url) as source:
        audio = recognizer.record(source)

        print("ಪ್ರಕ್ರಿಯಿಸಲಾಗುತ್ತಿದೆ...")

    try:
        # Recognize speech in Kannada
        text = recognizer.recognize_google(audio, language="kn-IN")

        # Print the recognized text
        print("ನೀವು ಹೇಳಿದ್ದೀರಿ:", text)

        # Detect the language of the recognized text
        translation = trans.detect(text)

        if translation.lang == 'kn':
            target_lang = 'hi'  # Translate to Hindi if Kannada is detected
        else:
            target_lang = 'kn'  # Translate to Kannada for other languages

        # Translate the recognized text to the target language
        translated_text = trans.translate(text, src=translation.lang, dest=target_lang).text

        # Speak the translated text in the chosen Indian language
        engine.say(translated_text)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("ಕ್ಷಮಿಸಿ, ಆಡಿಯೋವನ್ನು ಗ್ರಹಿಸಲಾಗಲಿಲ್ಲ.")

    except sr.RequestError as e:
        print(f"ಫಲಿತಾಂಶಗಳನ್ನು ವಿನಂತಿಸಲಾಗಲಿಲ್ಲ; {e}")

    except Exception as e:
        print(f"ತಪ್ಪಾಯಿತು: {e}")

# Call the function to start recognition and translation
recognize_and_translate()

    # Rest of your recognition and translation code here...

if __name__ == '__main__':
    # Assuming you have an audio_id from the server
    audio_id = 'some_unique_id'

    # Call the function to recognize and translate audio
    recognize_and_translate(audio_id)
