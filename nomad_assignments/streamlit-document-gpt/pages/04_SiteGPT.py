"""
- 입력으로 사용된 예시 Url
  - https://openai.com/index/introducing-gpts/
"""

import streamlit as st
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer

st.title('SiteGPT')
st.info("""
Ask questions about the content of a website.

👈 Start by writing the URL of the website on the sidebar
""")

html2text_transformer = Html2TextTransformer()

with st.sidebar:
    url = st.text_input("Wirte down a URL", placeholder="https://example.com")

if url:
    # async chromium loader
    loader = AsyncChromiumLoader([url])
    docs = loader.load()
    transformed = html2text_transformer.transform_documents(docs)
    st.write(transformed)

