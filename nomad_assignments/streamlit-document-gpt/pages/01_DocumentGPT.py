import os
from datetime import timedelta
from typing import Optional

import streamlit as st
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.scriptrunner import get_script_run_ctx


@st.cache_resource(show_spinner="Embedding file...", ttl=timedelta(hours=1))
def get_retriever_after_embedding(input_file, session_id):
    file_content = input_file.read()
    file_path = f"./.cache/files/{session_id}"
    file_full_path = f"{file_path}/{input_file.name}"
    embeddings_cache_dir = f'./.cache/embeddings/{session_id}'

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


def save_message_on_session(message, role):
    st.session_state["messages"].append({
        "message": message,
        "role": role,
    })


def paint_message(message, role):
    with st.chat_message(role):
        st.markdown(message)


def paint_history():
    for message in st.session_state["messages"]:
        paint_message(message["message"], message["role"])


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


class ChatCallbackHandler(BaseCallbackHandler):
    message = ""
    message_box: Optional[DeltaGenerator] = None

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        save_message_on_session(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


# init ###
# states
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# gpts
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1,
    streaming=True,
    callbacks=[
        ChatCallbackHandler(),
    ]
)
prompt = ChatPromptTemplate.from_messages([
    ('system', "You are a helpful assistant. Answer questions using only the following context. If you don't know the "
               "answer just say you don't know, don't make it up:\n\n{context}"),
    ('human', '{question}')
])


# views ###
st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📃",
)
st.title("DocumentGPT")
st.markdown("""
---
### Welcome!
- Use this chatbot to ask questions  to an AI about your files
- Upload your file on the sidebar.
---
""")

ctx = get_script_run_ctx()

with st.sidebar:
    st.write(f"your session uid: {ctx.session_id}")
    file = st.file_uploader("Upload your .txt file", type=['txt'])
    if st.button("Clear your chat histories"):
        st.session_state["messages"] = []

if file:
    retriever = get_retriever_after_embedding(file, ctx.session_id)

    if len(st.session_state["messages"]) <= 0:
        save_message_on_session("i'm ready! Ask away!", "ai")
    paint_history()

    input_message = st.chat_input("Ask anything about your file")
    if input_message:
        save_message_on_session(input_message, "human")
        paint_message(input_message, "human")

        chain = {
            'context': retriever | RunnableLambda(format_docs),
            'question': RunnablePassthrough()
        } | prompt | llm
        with st.chat_message("ai"):
            response = chain.invoke(input_message)

else:
    st.session_state["messages"] = []
