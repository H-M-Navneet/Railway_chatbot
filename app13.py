from flask import Flask, request, Response, jsonify
import speech_recognition as sr
from gtts import gTTS
import os
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
import pinecone

app = Flask(__name__)

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', 'c9be9891-57c9-4ace-a24b-47d7daea138a')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index_name = "railway-chatbot"

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Create a Pinecone index for document retrieval
docsearch = Pinecone.from_texts([], embeddings, index_name=index_name)

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

# Create a RetrievalQA instance
qa = RetrievalQA.from_chain_type(
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    chain_type_kwargs={"prompt": PROMPT}
)

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        # Initialize audio processing
        recognizer = sr.Recognizer()
        audio_file = request.files['audio']
        
        # Recognize audio from the uploaded file
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        
        language = "kannada"  # Replace with the desired language
        if language == "kannada":
            lang = "kn-IN"
        elif language == "hindi":
            lang = "hi-IN"
        else:
            lang = "en"
        
        text = recognizer.recognize_google(audio, language=lang)
        
        # Text processing (using the function defined below)
        answer_text = process_text_query(text)
        
        # Translate the answer back to the original language (if needed)
        if lang != "en":
            target_lang = lang
            # You need to add code to perform translation here.
            # 'answer_text' contains the answer in the original language.
        
        # Use text-to-speech to convert the response to audio
        output_audio = gTTS(text=answer_text, lang=lang, slow=False)
        
        # Get the audio as bytes
        audio_bytes = output_audio.get_wav_data()
        
        # Send the audio as a Flask response
        return Response(audio_bytes, mimetype="audio/wav")

    except Exception as e:
        return jsonify({"error": str(e)})

# Define the text processing function
def process_text_query(query):
    try:
        # Perform text processing and get the answer
        result = qa({"query": query})
        answer_text = result["result"]
        return answer_text
    except Exception as e:
        return str(e)

@app.route('/process-text', methods=['POST'])
def process_text():
    try:
        input_text = request.form['text']
        
        # Text processing (using the function defined below)
        answer_text = process_text_query(input_text)
        
        return jsonify({"response": answer_text})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
