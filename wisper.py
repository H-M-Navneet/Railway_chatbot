import whisper

# Create a Whisper recognizer
recognizer = whisper.WhisperRecognizer(languages=["en", "hi", "kn"])

# Start real-time transcription
with recognizer.listen(device="microphone"):
    # Speak into the microphone
    pass

# Print the transcription
transcription = recognizer.result

# If the transcription is not complete, wait for it to finish
while not transcription.finished:
    pass

# Print the final transcription
print(transcription.text)
