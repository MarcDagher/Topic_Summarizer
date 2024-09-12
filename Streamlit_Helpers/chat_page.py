import streamlit as st
from Streamlit_Helpers.api_functions import get_api_response, get_agent_image
from IPython.display import display

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
    col1, col2 = st.columns(spec=[2, 1], gap="large")  # Adjust the ratio to control the width

    # Add greeting in the first column
    with col1:
        st.markdown(
            """
            <div style="font-size: 20px; margin-top: 20px; text-align: center;">
                <div style="background-color: #F0F2F6; border-radius: 10px; padding: 30px;">
                    Hello, I am <strong>TopicSummarizer</strong> this is me in the picture🙃<br><br>
                    Ask me anything😊
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Add image in the second column
    with col2:
        try:
            image = get_agent_image()
            st.image(image.content, width=250)
        except:
            st.write("Image not available.")
    
  # Return adjusted session_state in order to update it in the app
  return session_state