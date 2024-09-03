import streamlit as st
from langchain_core.prompts import PromptTemplate

st.write("hello")
st.write([1, 2, 3, 4])

{"x": 1}
PromptTemplate
p = PromptTemplate.from_template("xxxx")
p # magic : write 호출 없이 그냥 이렇게 적는 것만으로 웹에 표시해줌 > 별로임 그냥 write 쓰자

st.selectbox(
    label="Choose your model",
    options=("GPT3", "GPT4")
)
