import streamlit as st
from Streamlit_Helpers.api_functions import get_api_response

## Handles Conversational UI 
def display_chat_page(session_state):

  # Add user's message to sessions_state
  if prompt := st.chat_input(placeholder = "Your message ..."): # (:= assigns chat_input's result to prompt while checking if its none)
    session_state.conversation.append({"role": "user", "content": prompt})

    ## Send user's message to the Agent, recieve Agent's response, and save the save the response in sessions_state
    api_output = get_api_response(user_message=prompt) # api_output: {response, conversation}
    
    # Check for returned errors
    if isinstance(api_output, str):
      session_state.conversation.append({"role": "assistant", "content": f"Somthing went wrong ({api_output})."})

    # Save response in session_state: messages
    else:
      ai_response = api_output['response'][-1]['content']
      session_state.conversation.append({"role": "assistant", "content": f"{ai_response}"})

  # Display Conversation in the UI
  for message in session_state.conversation:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])
  

  # Displays greeting UI if conversation is empty
  if len(session_state.conversation) == 0:
    # grey: #F0F2F6
    # red: #FF4B4B
    st.markdown(
      """
      <div style="font-size: 20px; margin-top: 20px; display: flex; justify-content: center; align-items: center; height: 100px;">
          <div style="text-align: center; background-color: #F0F2F6; border-radius: 10px; padding: 30px;">
              Hello, I am <strong>TopicSummarizer</strong>.<br>
              Please let me know when you're ready 😊.
          </div>
      </div>
      """, unsafe_allow_html=True
      )
    
  # Return adjust session_state in order to update it in the app
  print(f"\n\n\n--------{session_state['conversation']}")
  return session_state