import pyttsx3

engine = pyttsx3.init()

# Set the properties for Indian languages
engine.setProperty('rate', 150)  # Adjust speech rate as needed
engine.setProperty('volume', 1)  # Adjust volume as needed

# List available voices
voices = engine.getProperty('voices')

# Choose an Indian language voice (e.g., Hindi or Tamil)
# You may need to specify the index of the desired voice from the 'voices' list
# For Hindi, you might use voices[0]
# For Tamil, you might use voices[1]
engine.setProperty('voice', voices[0])  # Adjust the index as needed

# Text to be spoken in the chosen Indian language
text = "नमस्ते दोस्तों, आप कैसे हैं?"  # Replace with your Indian language text

engine.say(text)

# Wait for the speech to finish
engine.runAndWait()
