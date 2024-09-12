import streamlit as st
from Streamlit_Helpers.api_functions import get_api_response
 
def display_chat_page(session_state):

  if prompt := st.chat_input(placeholder = "Your message ..."): # (:= assigns chat_input's result to prompt while checking if its none)

    session_state.conversation.append({"role": "user", "content": prompt})
    api_output = get_api_response(user_message=prompt) # api_output: {response}
    
    # Check for returned errors
    if isinstance(api_output, str):
      session_state.conversation.append({"role": "assistant", "content": f"Somthing went wrong ({api_output})."})

    # Save response in session_state: conversation
    else:
      ai_response = api_output['response'][-1]['content']
      session_state.conversation.append({"role": "assistant", "content": f"{ai_response}"})

  # Display Conversation in the UI
  for message in session_state.conversation:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])
  

  # Displays greeting UI if conversation is empty
  if len(session_state.conversation) == 0:
    # grey: #F0F2F6 - red: #FF4B4B
    st.markdown(
      """
      <div style="font-size: 20px; margin-top: 20px; display: flex; justify-content: center; align-items: center; height: 100px;">
          <div style="text-align: center; background-color: #F0F2F6; border-radius: 10px; padding: 30px;">
              Hello, I am <strong>TopicSummarizer</strong>.<br>
              Ask me anything😊.
          </div>
      </div>
      """, unsafe_allow_html=True
      )
    
  # Return adjust session_state in order to update it in the app
  print(f"\n\n\n--------{len(session_state['conversation'])}")
  return session_state