"""
- model tokens comparison: https://platform.openai.com/docs/models/gpt-4o-mini
"""

import os
from datetime import timedelta

import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx


@st.cache_resource(show_spinner="Separated file...", ttl=timedelta(hours=1))
def split_files(input_file, session_id):
    file_content = input_file.read()
    file_path = f"./.cache/quiz_files/{session_id}"
    file_full_path = f"{file_path}/{input_file.name}"

    os.makedirs(file_path, exist_ok=True)

    with open(file_full_path, "w") as target_file:
        target_file.write(file_content.decode("utf-8"))

    character_text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o-mini",
        chunk_size=600,
        chunk_overlap=100,
        separator="\n",
    )
    loader = TextLoader(file_full_path)
    return loader.load_and_split(text_splitter=character_text_splitter)


def format_docs(documents):
    return "\n\n".join(document.page_content for document in documents)


# states
ctx = get_script_run_ctx()
docs = None
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.1,
)

# views
st.set_page_config(
    page_title="Quiz GPT",
    page_icon="🧐"
)
st.title("🧐 Quiz GPT")

with st.sidebar:
    choice = st.selectbox("Choose what you want to use.", (
        "File", "Wikipedia Article",
    ), )

    if choice == "File":
        file = st.file_uploader("Upload a .txt file", type=["txt"])
        if file:
            with st.status("Splitting the file"):
                docs = split_files(file, ctx.session_id)
    elif choice == "Wikipedia Article":
        topic = st.text_input("Name of the article")
        retriever = WikipediaRetriever(top_k_results=5)
        if topic:
            with st.status("Searching wikipedia"):
                docs = retriever.get_relevant_documents(topic)

if docs:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a helpful assistant that is role playing as a teacher.
     
Based ONLY on the following context make 10 questions to test the user's knowledge about the text.

Each question should have 4 answers, three of them must be incorrect and one should be correct.
     
Use (o) to signal the correct answer.
     
Question examples:
     
Question: What is the color of the ocean?
Answers: Red|Yellow|Green|Blue(o)
     
Question: What is the capital or Georgia?
Answers: Baku|Tbilisi(o)|Manila|Beirut
     
Question: When was Avatar released?
Answers: 2007|2001|2009(o)|1998
     
Question: Who was Julius Caesar?
Answers: A Roman Emperor(o)|Painter|Actor|Model
     
Your turn!
     
Context: {context}
""")
    ])
    chain = {"context": format_docs} | prompt | llm

    start = st.button("Generate Quiz")
    if start:
        results = chain.invoke(docs)
        st.write(results.content.split("\n\n"))
else:
    st.info("""
    I will make a quiz from Wikipedia articles of files you upload to test
    your knowledge and help you study. 
    
    Get started by uploading a file or searching on Wikipedia in the sidebar. 🔍
    """)
