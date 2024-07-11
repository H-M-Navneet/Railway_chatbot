from flask import Flask, request, Response, jsonify
import speech_recognition as sr
from gtts import gTTS
from flask_cors import CORS
import os
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
import pinecone
from googletrans import Translator
from langchain.llms import CTransformers

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '1acea4e0-c639-4577-b431-6d607796e5d5')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index_name = "railway-chatbot"

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Create a Pinecone index for document retrieval
docsearch = Pinecone.from_existing_index(index_name, embeddings)

# Create a template for processing user queries
prompt_template = """
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that I don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs = {"prompt": PROMPT}

llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens': 512,
                            'temperature': 0.8})

# Create a RetrievalQA instance
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 1}),
    chain_type_kwargs={"prompt": PROMPT}
)


@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        # Initialize audio processing
        recognizer = sr.Recognizer()
        audio_file = request.files['audio']

        # Save the received audio blob locally before processing
        audio_path_before = "received_audio_before.wav"
        audio_file.save(audio_path_before)

        # Recognize audio from the uploaded file
        with sr.AudioFile(audio_path_before) as source:
            audio = recognizer.record(source)

        language = "kannada"
        if language == "kannada":
            lang = "kn-IN"
        elif language == "hindi":
            lang = "hi-IN"
        else:
            lang = "en"

        text = recognizer.recognize_google(audio, language=lang)

        # Translate the answer back to the original language
        trans = Translator()

        if lang == "kn-IN":
            lang = "kn"

        elif lang == "hi-IN":
            lang = "hi"

        if lang == "kn":
            target_lang = "en"
            text = trans.translate(text, src=lang, dest=target_lang).text

        elif lang == "hi":
            target_lang = "en"
            text = trans.translate(text, src=lang, dest=target_lang).text

        try:
            # Perform text processing and get the answer
            result = qa({"query": text})
            answer_text = result["result"]

            # Translate the answer back to the original language
            text = trans.translate(answer_text, src="en", dest=lang).text

            # Use text-to-speech to convert the response to audio
            tts = gTTS(text, lang=lang, slow=False)

            # Save the processed audio locally
            audio_path_after = "processed_audio_after.wav"
            tts.save(audio_path_after)

            # Get the processed audio as bytes
            with open(audio_path_before, 'rb') as audio_path_before:
                audio_bytes = audio_path_before.read()
            k="audio processed"
            # Send the processed audio as a Flask response
            return Response(k, mimetype="text/plain")
        except Exception as e:
            return str(e)
        

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/get-processed-audio', methods=['GET'])
def get_processed_audio():
    try:
        # Send the processed audio file as a response
        #return send_file("processed_audio_after.wav", mimetype="audio/wav")
        return send_file("processed_audio_after.wav", mimetype="audio/wav")

    except Exception as e:
        return str(e)    

from flask import Flask, send_file


@app.route('/audio')
def send_audio():
    audio_file_path = 'processed_audio_after.wav'  # Replace with the actual path to your audio file
    return send_file(audio_file_path, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)
