import streamlit as st
from datetime import datetime

# 데이터가 변경될 때 마다 streamlit home.py 파일 전체가 다시 실행됨 흐음....

st.title(datetime.now())

model = st.selectbox(
    label="Choose your model",
    options=("GPT3", "GPT4")
)
if model == "GPT3":
    st.write("cheap")
else:
    st.write("not cheap...")

name = st.text_input("What is your name?")
st.write(name)

value = st.slider("temperature", min_value=0.0, max_value=1.0)
st.write(f"temperature: {value}")
