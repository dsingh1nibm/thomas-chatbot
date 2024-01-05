import os
import streamlit as st
from io import StringIO
import re
import sys
import pickle
from datetime import datetime
from modules.chatbot import Chatbot
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
st.set_page_config(layout="wide", page_icon="💬", page_title="Thomas | Chat-Bot 🤖" )
# st.markdown(
#     """
# <style>
#     [data-testid="stDecoration"] {
#         position: sticky;
#         top: 0rem;
#         background-color: #3A6DAB;
#         z-index: 999999;
        
        
#     }
#      [data-testid="stHeader"] {
#         position: sticky;
#         top: 0rem;
#         background-color: #3A6DAB;
#         z-index: 999999;
#         height: 90px
#     }
  
# </style>
#     """,
#     unsafe_allow_html=True
# )

#To be able to update the changes made to modules in localhost (press r)
def reload_module(module_name):
    import importlib
    import sys
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

history_module = reload_module('modules.history')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

ChatHistory = history_module.ChatHistory
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# with open( "css/style.css" ) as css:
#     st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header("TXT")

user_api_key = utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()
else:
    # st.session_state.setdefault("reset_chat", False)
    os.environ["OPENAI_API_KEY"] = user_api_key
    sidebar.show_options()    
    history = ChatHistory()       
    uploaded_files = utils.handle_upload(["txt"])
    if (uploaded_files):
        chatbot = utils.setup_chatbot(st.session_state["model"], st.session_state["temperature"], "TXT")
        st.session_state["chatbot"] = chatbot
    dirTextPath = os.getcwd()+"/embeddings"+"/"+str(st.session_state.api_key)+"/Text"
    filename=st.session_state.api_key
    if os.path.exists(dirTextPath):
       if os.path.isfile(f"{dirTextPath}/{filename}.pkl"):
        try:
            st.session_state["ready"] = True        
            with open(f"{dirTextPath}/{filename}.pkl", "rb") as f:
                vectors = pickle.load(f)
            chatbot = Chatbot(st.session_state["model"], st.session_state["temperature"],vectors)
            st.session_state["chatbot"] = chatbot            
            if st.session_state["ready"]:
                # Create containers for chat responses and user prompts
                response_container, prompt_container = st.container(), st.container()
                with prompt_container:
                    # Display the prompt form
                    is_ready, user_input = layout.prompt_form()
                    if 'Page' not in st.session_state:
                        st.session_state["Page"]=["Text"]
                    # if st.session_state["Page"]==["Text"]:
                    #     st.session_state["Page"]=["PDF"]
                        
                    if "user" not in st.session_state:
                        st.session_state["user"] = ["Hey Thomas ! 👋"]
                    if "assistant" not in st.session_state:
                        st.session_state["assistant"] = ["Hello ! Ask me anything from text documents"]


                    # Reset the chat history if button clicked
                    if st.session_state["reset_chat"]:
                        st.session_state["history"] = []       
                        st.session_state["user"] = ["Hey Thomas ! 👋"]
                        st.session_state["assistant"] = ["Hello ! Ask me anything from text documents"]
                        #st.session_state["reset_chat"] = False
                    #     history.reset(uploaded_files)

                    if is_ready:
                        # Update the chat history and display the chat messages
                        history.append("user", user_input)

                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()

                        output = st.session_state["chatbot"].conversational_chat(user_input)

                        sys.stdout = old_stdout

                        history.append("assistant", output)

                        # Clean up the agent's thoughts to remove unwanted characters
                        thoughts = captured_output.getvalue()
                        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                        # Display the agent's thoughts
                        with st.expander("Display the agent's thoughts"):
                            st.write(cleaned_thoughts)
                history.generate_messages(response_container)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    


