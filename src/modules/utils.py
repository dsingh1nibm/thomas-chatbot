import os
import pandas as pd
import streamlit as st
import pdfplumber

from modules.chatbot import Chatbot
from modules.embedder import Embedder
from datetime import datetime
from PyPDF2 import PdfReader

class Utilities:        

    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None
        #you can define your API key in .env directly
        # if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
        #     user_api_key = os.environ["OPENAI_API_KEY"]
        #     # st.sidebar.success("API key loaded from .env", icon="🚀")
        # else:
        if st.session_state.api_key is not None:
            user_api_key = st.session_state.api_key
            # st.sidebar.success("API key loaded from previous input", icon="🚀")
        else:
            user_api_key = st.sidebar.text_input(
                label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
            )
            if user_api_key:
                st.session_state.api_key = user_api_key
                dirpath= os.getcwd()+"/"+user_api_key
                isExist = os.path.exists(dirpath)
                if not isExist:
                    # Create a new directory because it does not exist
                    os.makedirs(dirpath)                        
        return user_api_key

    
    @staticmethod
    def handle_upload(file_type):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """        
        uploaded_files = st.sidebar.file_uploader("upload", type=file_type, label_visibility="hidden", accept_multiple_files=True)
        
        if len(uploaded_files):            
            # Hide filename on UI
            st.markdown('''
                <style>
                .uploadedFile {display: none}
            <style>''',
            unsafe_allow_html=True)
            
            def upload_pdf_files(uploaded_file):
                pdfdirpath=os.getcwd()+"/"+str(st.session_state.api_key)+"/Docs/PDFs"
                isExist = os.path.exists(pdfdirpath)
                if not isExist:                    
                    os.makedirs(pdfdirpath)
                with open(os.path.join(pdfdirpath,uploaded_file.name),"wb") as f:  f.write((uploaded_file).getbuffer())           
            
            def upload_txt_files(uploaded_file):
                txtdirpath=os.getcwd()+"/"+str(st.session_state.api_key)+"/Docs/Text"                
                isExist = os.path.exists(txtdirpath)
                if not isExist:                    
                    os.makedirs(txtdirpath)
                with open(os.path.join(txtdirpath,uploaded_file.name),"wb") as f:  f.write((uploaded_file).getbuffer())
            
            def upload_excel_files(uploaded_file):
                exceldirpath=os.getcwd()+"/"+str(st.session_state.api_key)+"/Docs/Excel"                
                isExist = os.path.exists(exceldirpath)
                if not isExist:                    
                    os.makedirs(exceldirpath)
                with open(os.path.join(exceldirpath,uploaded_file.name),"wb") as f:  f.write((uploaded_file).getbuffer())        
                
            for uploaded_file in uploaded_files:
                if "pdf" in file_type : 
                    upload_pdf_files(uploaded_file)
                elif "txt" in file_type : 
                    upload_txt_files(uploaded_file)
                elif "csv" in file_type : 
                    upload_excel_files(uploaded_file)
                elif "xls" in file_type : 
                    upload_excel_files(uploaded_file)
                elif "xlsx" in file_type : 
                    upload_excel_files(uploaded_file)
            st.sidebar.markdown('Upload complete!')        
           
        dirpath= os.getcwd()+"/"+str(st.session_state.api_key)
        if "pdf" in file_type :             
            dirfilespath= dirpath+"/Docs/PDFs/" 
        elif "txt" in file_type : 
            dirfilespath= dirpath+"/Docs/Text/" 
        elif "csv" in file_type : 
            dirfilespath= dirpath+"/Docs/Excel/" 
        elif "xls" in file_type : 
            dirfilespath= dirpath+"/Docs/Excel/" 
        elif "xlsx" in file_type : 
            dirfilespath= dirpath+"/Docs/Excel/" 
        isExist = os.path.exists(dirfilespath)
        if isExist:               
            files = os.listdir(f"{dirfilespath}")                             
            for f in files:                
                st.sidebar.checkbox(f, key=f)              
            # if files:
            #     if 'clicked' not in st.session_state:
            #         st.session_state.clicked = False
            #     def click_button():
            #         st.session_state.clicked = True
            #     st.sidebar.button("Delete", key="Delete", on_click=click_button)            
            # if st.session_state.clicked:                    
            #     st.sidebar.markdown('Delete clicked!')
            #     st.session_state.clicked = False
        return uploaded_files        
    
    @staticmethod
    def setup_chatbot(model, temperature, type):
        """
        Sets up the chatbot with the uploaded files, model, and temperature
        """
        embeds = Embedder()       

        def get_text(files):
            def get_file_extension(file):
                return os.path.splitext(file)[1].lower()
            text = ""
            dirpath= os.getcwd()+"/"+str(st.session_state.api_key) 
           
            for file in files:
                ext= get_file_extension(file)                
                if ext==".pdf":
                    with open(f"{dirpath}/Docs/PDFs/{file}", "rb") as filehandle:
                        file_reader = PdfReader(filehandle)                    
                        for page in file_reader.pages:
                            text += page.extract_text()
                elif  ext==".txt": 
                    with open(f"{dirpath}/Docs/Text/{file}", "rb") as filehandle:                        
                        text += filehandle.read().decode("utf-8")      
            return text
            
        with st.spinner("Processing..."):
            dirpath= os.getcwd()+"/"+str(st.session_state.api_key)
            if type == "TXT":
                dirtxtpath= dirpath+"/Docs/Text/"               
                files = os.listdir(f"{dirtxtpath}")                    
            elif type == "PDF" :
                dirpdfpath= dirpath+"/Docs/PDFs/"               
                files = os.listdir(f"{dirpdfpath}")
            
            text= get_text(files)
            filename=st.session_state.api_key           
            # Get the document embeddings for the uploaded files
            vectors = embeds.getDocEmbeds(text, filename, type)                
            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature,vectors)
            st.session_state["ready"] = True
            return chatbot

    @staticmethod
    def remote_css(url):
        st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

    
