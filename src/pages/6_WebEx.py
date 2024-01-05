import os
import streamlit as st
from datetime import datetime
from modules.layout import Layout
from modules.utils import Utilities
from modules.converter import vtt_to_txt
from modules.summarizer import generate_summary
from modules.splitter import split_transcript

st.set_page_config(layout="wide", page_icon="💬", page_title="Thomas | Chat-Bot 🤖")
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Instantiate the main components
layout, utils = Layout(), Utilities()
st.markdown(
    f"""
    <h1 style='text-align: center;'> Ask Thomas to convert/summarize webex recording !</h1>
    """,
    unsafe_allow_html=True,
)

user_api_key = utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()

else:
    os.environ["OPENAI_API_KEY"] = user_api_key
    webex_url = st.text_input(placeholder="Enter Webex Recording URL", label_visibility="hidden", label =" ")
    # option = st.selectbox(
    #     'Select',
    #     ('Convert', 'Summarize'))
    dirpath= os.getcwd()   
    filename=datetime.now().strftime("%Y%m%d") 
    output_base=f"{dirpath}/Docs/Recording/output"
    summary_output = f"{output_base}/{filename}_summary.txt"
    fileExist= os.path.isfile(summary_output)
    if not fileExist :
    # if option == 'Convert':
        
    #     #Convert the .vtt file to a .txt file                    
    #     output_base=f"{dirpath}/Docs/Recording/output"
    #     input_base=f"{dirpath}/Docs/Recording/input/sample9.vtt"        
    #     convert_output = f"{output_base}/{filename}_transcript.txt"
    #     vtt_to_txt(input_base, convert_output)

    # elif option == 'Summarize':
        
    
        input_base=f"{dirpath}/Docs/Recording/input/sample9.vtt"        
        convert_output = f"{output_base}/{filename}_transcript.txt"
        raw_txt = vtt_to_txt(input_base, convert_output)
        docs = split_transcript(raw_txt)
        
        # Unpack the tuple returned by generate_summary
        summary_md, token_info = generate_summary(docs)
        
        
        # with open(summary_output, 'w') as file:
        #     file.write(summary_md)

        # token_info_output = f"{output_base}/{filename}_token_info.txt"
        # with open(token_info_output, 'w') as file:
        #     for key, value in token_info.items():
        #         file.write(f"{key}: {value}\n")

        # st.write(summary_md)
    else:
        with open(summary_output, "r") as f:
            markdown_text = f.read()
            st.write(markdown_text)
