import speech_recognition as sr

r = sr.Recognizer()

audio_file_path = "processed_audio_after.wav"

try:
    with sr.AudioFile(audio_file_path) as source:
        audio = r.listen(source)
        text = r.recognize_google(audio, language="en")
        print("Transcription: {}".format(text))

except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio or no speech detected")

except FileNotFoundError:
    print("File not found: {}".format(audio_file_path))

except Exception as e:
    print("An error occurred: {}".format(e))
