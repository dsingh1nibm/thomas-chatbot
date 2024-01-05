import base64
import os
import importlib
#import genai
import sys
import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime
from modules.robby_sheet.table_tool import PandasAgent
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar

def reload_module(module_name):
    """For update changes
    made to modules in localhost (press r)"""

    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

table_tool_module = reload_module('modules.robby_sheet.table_tool')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')


st.set_page_config(layout="wide", page_icon="💬", page_title="Thomas | Chat-Bot 🤖")
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# background_image_path = "C:/Users/04318A744/Desktop/Multidatasource/Robby-chatbot/images/Bestseller.jpg"
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#         return base64.b64encode(data).decode()

# def set_png_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file)
#     page_bg_img = """
#         body {
# background-image: url("data:image/jpeg;base64,%s");
# background-size: cover;
# }
# """% bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)
#     return

# set_png_as_page_bg(background_image_path)
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
#         height: 90px;       
#     }
  
# </style>
#     """,
#     unsafe_allow_html=True
# )

layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header("CSV, Excel")

user_api_key = utils.load_api_key()
os.environ["OPENAI_API_KEY"] = user_api_key


if not user_api_key:
    layout.show_api_key_missing()

else:
    # client = genai.Client
    st.session_state.setdefault("reset_chat", False)
    sidebar.show_options()
    history = ChatHistory()   
    uploaded_files = utils.handle_upload(["csv","xls","xlsx"]) 
    filename=st.session_state.api_key
    dirExcelPath = os.getcwd()+"/embeddings"+"/"+str(st.session_state.api_key)+"/Excel"   
    if uploaded_files:
        if not os.path.isfile(f"{dirExcelPath}/{filename}.pkl"):
            def get_file_extension(file):
                    return os.path.splitext(file)[1].lower()
            combined_df = pd.DataFrame()
            # df = pd.read_excel(files)
            # summary = client.summarize(df)
            # combined_df = pd.DataFrame(summary)
            dirpath= os.getcwd()+"/"+str(st.session_state.api_key)
            files=os.listdir(f"{dirpath}/Docs/Excel/")
            for file in files:
                ext= get_file_extension(file)                
                if ext==".csv":                    
                    df = pd.read_csv(f"{dirpath}/Docs/Excel/{file}")
                    combined_df = pd.concat([combined_df, df])
                elif ext == ".xlsx":
                    df = pd.read_excel(f"{dirpath}/Docs/Excel/{file}")
                    combined_df = pd.concat([combined_df, df])
            if not os.path.exists(dirExcelPath):
                os.makedirs(dirExcelPath)
            combined_df.to_pickle(f"{dirExcelPath}/{filename}.pkl")
    if os.path.exists(dirExcelPath):
       if os.path.isfile(f"{dirExcelPath}/{filename}.pkl"):
        try:
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []
            csv_agent = PandasAgent()
            df=pd.read_pickle(f"{dirExcelPath}/{filename}.pkl")
            with st.form(key="query"):
                query = st.text_input("", value="", type="default", placeholder="Ask me ...")
                submitted_query = st.form_submit_button("Submit")
                reset_chat_button = st.form_submit_button("Reset Chat")
                if reset_chat_button:
                    st.session_state["chat_history"] = []
        
            if submitted_query:            
                result, captured_output = csv_agent.get_agent_response(df , query)
                # cleaned_thoughts = csv_agent.process_agent_thoughts(captured_output)
                # csv_agent.display_agent_thoughts(cleaned_thoughts)
                csv_agent.update_chat_history(query, result)
                csv_agent.display_chat_history()
            if df is not None:
                st.subheader("Current dataframe:")
                st.write(df)
        except Exception as e:
            st.error(f"Error: {str(e)}")
