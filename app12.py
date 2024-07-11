from flask import Flask, request, Response, jsonify
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import os
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from dotenv import load_dotenv

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

chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})

# Create a RetrievalQA instance
qa = RetrievalQA.from_chain_type(llm=llm, 
                                chain_type="stuff",
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
        
        language = "kannada"
        if language == "kannada":
            lang = "kn-IN"
        elif language == "hindi":
            lang = "hi-IN"
        else:
            lang = "en"
        
        text = recognizer.recognize_google(audio, language=lang)
        
        # Text processing (using the function defined below)
        answer_text = process_text_query(text)

        import googletrans
        from googletrans import Translator
        trans = Translator()
        
        # Translate the answer back to the original language
        if lang != "en":
            target_lang = lang
            answer_text = trans.translate(answer_text, src="en", dest=target_lang).text
        
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

if __name__ == '__main__':
    app.run(debug=True)
