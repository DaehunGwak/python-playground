import os

import streamlit as st
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from streamlit.runtime.scriptrunner import get_script_run_ctx


def embed_file(input_file):
    file_content = input_file.read()
    file_path = f"./.cache/files/{ctx.session_id}"
    file_full_path = f"{file_path}/{input_file.name}"
    embeddings_cache_dir = f'./.cache/embeddings/{ctx.session_id}'

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if not os.path.exists(embeddings_cache_dir):
        os.makedirs(embeddings_cache_dir)

    with open(file_full_path, "w") as target_file:
        target_file.write(file_content.decode("utf-8"))

    character_text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-3.5-turbo",
        chunk_size=600,
        chunk_overlap=100,
        separator="\n",
    )
    loader = TextLoader(file_full_path)
    seperated_docs = loader.load_and_split(text_splitter=character_text_splitter)

    openai_3_small_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    file_store = LocalFileStore(f'{embeddings_cache_dir}/{input_file.name}')
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=openai_3_small_embeddings,
        document_embedding_cache=file_store
    )

    vectorstore = Chroma.from_documents(embedding=cached_embeddings, documents=seperated_docs)
    return vectorstore.as_retriever()


st.title("DocumentGPT")

st.markdown("""
Welcome!

Use this chatbot to ask questions  to an AI about your files
""")

ctx = get_script_run_ctx()
st.write(f"your session uid: {ctx.session_id}")

file = st.file_uploader("Upload your .txt file", type=['txt'])

if file:
    retriever = embed_file(file)
    docs = retriever.invoke("winston")
    st.write(docs)