"""
- 입력으로 사용된 예시 Url
  - blog: https://openai.com/index/introducing-gpts/
  - sitemap: https://openai.com/sitemap.xml > 보안 이슈로 막힌 듯?
  - 과제 sitemap: https://developers.cloudflare.com/sitemap-0.xml
- trouble shooting
  - python SSL: https://coinpipe.tistory.com/171
  - user-agent issue: `poetry add fake_useragent`
"""
from datetime import timedelta

import streamlit as st
from fake_useragent import UserAgent
from langchain_community.document_loaders import SitemapLoader
from langchain_core.documents import Document

user_agent = UserAgent()


@st.cache_resource(
    show_spinner="Sitemap 분석은 시간이 오래걸리니 30분 정도 커피드시고 오시는건 어떨까요? ☕️",
    ttl=timedelta(hours=12),
)
def load_website(target_url: str) -> list[Document]:
    loader = SitemapLoader(target_url)
    loader.requests_per_second = 3
    loader.header = {'User-Agent': user_agent.random}
    return loader.load()


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
        st.write(docs)
