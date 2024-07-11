from functools import lru_cache

@lru_cache(maxsize=None)
def ques(language,prompt):
    
    from langchain import PromptTemplate
    from langchain.chains import RetrievalQA
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import Pinecone
    import pinecone
    from langchain.document_loaders import PyPDFLoader, DirectoryLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.prompts import PromptTemplate
    from langchain.llms import CTransformers
    from langchain.chat_models import ChatOpenAI
    from transformers import AutoTokenizer
    from dotenv import load_dotenv
    import os
    import timeit
    import sys

    load_dotenv()
    PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY','1acea4e0-c639-4577-b431-6d607796e5d5')
    PINECONE_API_ENV=os.environ.get('PINECONE_API_ENV', 'gcp-starter')

    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    pinecone.init(api_key=PINECONE_API_KEY,
                environment=PINECONE_API_ENV)

    index_name="railway-chatbot"

    #docsearch = Pinecone.from_texts(split_docs, embeddings, index_name=index_name)
    docsearch=Pinecone.from_existing_index(index_name, embeddings)

    prompt_template="""
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that I don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """

    PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    chain_type_kwargs={"prompt": PROMPT}

    llm=CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens':512,
                            'temperature':0.8})

    qa=RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={'k': 1}),return_source_documents=True, chain_type_kwargs=chain_type_kwargs)

    import googletrans
    from googletrans import Translator

    trans = Translator()

    if language=="Kannada(ಕನ್ನಡ)":
        lang="kn"

    elif language=="Hindi(हिंदी)":
        lang="hi"

    elif language=="English":
        lang="en"

    if lang=="kn":
        target_lang = "en"
        prompt = trans.translate(prompt, src=lang, dest=target_lang).text

    elif lang=="hi":
        target_lang = "en"
        prompt = trans.translate(prompt, src=lang, dest=target_lang).text

    #print(text)

    user_input=prompt
    if user_input=='exit':
        print('Exiting')
        sys.exit()
    result=qa({"query": user_input})
    #print("Response : ", result["result"])

    res_text = trans.translate(result["result"], src="en", dest=lang).text

    return res_text

import streamlit as st

language = st.sidebar.radio("Select Language",["English","Hindi(हिंदी)","Kannada(ಕನ್ನಡ)"])

st.title("Railway Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("what is up ?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role":"user","content":prompt})

    response = ques(language,prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role":"assistant","content":response})