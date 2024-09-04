import streamlit as st
from datetime import datetime

# st.title("Sidebar Test")
# st.write(datetime.now())

# sidebar option 1
# st.sidebar.title('sidebar title')
# st.sidebar.write('write test')

# with st.sidebar:
#     st.title('sidebar title')
#     st.write(datetime.now())
#
# tab_one, tab_two, tab_three = st.tabs(['A', 'B', 'C'])
#
# with tab_one:
#     st.write('a')
# with tab_two:
#     st.write('b')
# with tab_three:
#     st.write('c')

st.set_page_config(
    page_title="FullstackGPT Home",
    page_icon="🫠"
)

st.title("FullstackGPT Home")
