import streamlit as st
from Streamlit_Helpers.chat_page import display_chat_page

#########################################
# Initialize Streamlit's Sesstion State #
#########################################
if not ("pages") in st.session_state:
  st.session_state.current_page = "chat"

if "conversation" not in st.session_state:
  st.session_state.conversation = []

##############
# Display UI #
##############

# Chat Page
if st.session_state.current_page == 'chat':
  st.session_state = display_chat_page(session_state=st.session_state)