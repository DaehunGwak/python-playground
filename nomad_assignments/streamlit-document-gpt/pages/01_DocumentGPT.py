import streamlit as st
import time

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def draw_message(message, role):
    with st.chat_message(role):
        st.write(message)


def save_message(message, role):
    st.session_state["messages"].append({
        "message": message,
        "role": role,
    })


st.title("DocumentGPT")

for _message in st.session_state["messages"]:
    draw_message(_message['message'], _message['role'])

input_message = st.chat_input("Send a message to the ai")

if input_message:
    draw_message(input_message, "human")
    save_message(input_message, "human")
    time.sleep(2)
    draw_message(f"You said: {input_message}", "ai")
    save_message(f"You said: {input_message}", "ai")

# with st.status("Embeding file...", expanded=True) as status:
#     time.sleep(3)
#     st.write("Getting the file")
#     time.sleep(3)
#     st.write("Embedding the file")
#     time.sleep(3)
#     st.write("Caching the file")
#     status.update(label="Error", state="error")
