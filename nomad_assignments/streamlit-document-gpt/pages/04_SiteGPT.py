"""
- 입력으로 사용된 예시 Url
  - blog: https://openai.com/index/introducing-gpts/
  - sitemap: https://openai.com/sitemap.xml > 보안 이슈로 막힌 듯?
  - 과제 sitemap: https://developers.cloudflare.com/sitemap-0.xml
  - 내 과거: https://daehungwak.github.io/til/sitemap.xml
- troubleshooting
  - python SSL: https://coinpipe.tistory.com/171
  - user-agent issue: `poetry add fake_useragent`
"""
from datetime import timedelta

import streamlit as st
from fake_useragent import UserAgent
from langchain_community.document_loaders import SitemapLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

user_agent = UserAgent()


def parse_page(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return (
        str(soup.get_text())
        .replace("\n", " ")
        .replace("\xa0", " ")
    )


@st.cache_resource(
    show_spinner="Sitemap 분석은 시간이 오래걸리니 10분 정도 커피드시고 오시는건 어떨까요? ☕️",
    ttl=timedelta(hours=12),
)
def load_website(target_url: str) -> list[Document]:
    _splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o-mini",
        chunk_size=1000,
        chunk_overlap=100,
    )
    _loader = SitemapLoader(target_url, parsing_function=parse_page)
    _loader.requests_per_second = 2
    _loader.header = {'User-Agent': user_agent.random}
    return _loader.load_and_split(text_splitter=_splitter)


@st.cache_resource(
    show_spinner="로드한 sitemap 문서들을 임베딩하고 있습니다 👩🏻‍🔧",
    ttl=timedelta(hours=12),
)
def get_retriever(target_url: str, _target_docs: list[Document]) -> VectorStoreRetriever:
    _vector_store = FAISS.from_documents(
        documents=_target_docs,
        embedding=GPT4AllEmbeddings()
    )
    return _vector_store.as_retriever()


st.set_page_config(
    page_title="SiteGPT",
    page_icon="🖥️",
)
st.title('SiteGPT')
st.info("""
Ask questions about the content of a website.

👈 Start by writing the URL of the website on the sidebar
""")


with st.sidebar:
    url = st.text_input("Write down a URL", placeholder="https://example.com")

if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        docs = load_website(url)
        retriever = get_retriever(url, docs)
        result_docs = retriever.invoke('클린 코드가 뭐야?')
        st.write(result_docs)
