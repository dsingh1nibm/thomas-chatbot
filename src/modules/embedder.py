import os
import streamlit as st
import pickle
import tempfile
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

class Embedder:

    def __init__(self):
        self.PATH = os.getcwd()+"/embeddings"+"/"+str(st.session_state.api_key)+"/Text"
        # self.createEmbeddingsDir()

    def createEmbeddingsDir(self):
        """
        Creates a directory to store the embeddings vectors
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def storeDocEmbeds(self, file, original_filename, type):
        """
        Stores document embeddings using Langchain and FAISS
        """
        
        # with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
        #     tmp_file.write(file)
        #     tmp_file_path = tmp_file.name
            
        # def get_file_extension(uploaded_file):
        #     file_extension =  os.path.splitext(uploaded_file)[1].lower()
            
        #     return file_extension
        
        text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size = 2000,
                chunk_overlap  = 100,
                length_function = len
            )
            
        chunks = text_splitter.split_text(file)
        
        # file_extension = get_file_extension(original_filename)

        # if file_extension == ".csv":
        #     loader = CSVLoader(file_path=tmp_file_path, encoding="latin1",csv_args={
        #         'delimiter': ',',})
        #     data = loader.load()

        # elif file_extension == ".pdf":
        # loader = PyPDFLoader(file_path=tmp_file_path)  
        # data = loader.load_and_split(text_splitter)
        
        # elif file_extension == ".txt":
        #     loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
        #     data = loader.load_and_split(text_splitter)
            
        embeddings = OpenAIEmbeddings()
        
        vectors = FAISS.from_texts(chunks, embeddings)
        
        
        # os.remove(tmp_file_path)

        # Save the vectors to a pickle file
        if type == "PDF":
            dirTextPath = os.getcwd()+"/embeddings"+"/"+str(st.session_state.api_key)+"/PDF"
            with open(f"{dirTextPath}/{original_filename}.pkl", "wb") as f:
                pickle.dump(vectors, f)
        elif type == "TXT":
            dirTextPath = os.getcwd()+"/embeddings"+"/"+str(st.session_state.api_key)+"/Text"
            with open(f"{dirTextPath}/{original_filename}.pkl", "wb") as f:
                pickle.dump(vectors, f)

    def getDocEmbeds(self, file, original_filename, type):
        """
        Retrieves document embeddings
        """
        if type == "PDF":
            dirPDFPath = os.getcwd()+"/embeddings"+"/"+str(st.session_state.api_key)+"/PDF"
            if not os.path.exists(dirPDFPath):
                os.makedirs(dirPDFPath)
            self.storeDocEmbeds(file, original_filename, "PDF")
            with open(f"{dirPDFPath}/{original_filename}.pkl", "rb") as f:
                # Load the vectors from the pickle file
                vectors = pickle.load(f)
        elif type == "TXT":
            dirTextPath = os.getcwd()+"/embeddings"+"/"+str(st.session_state.api_key)+"/Text"
            if not os.path.exists(dirTextPath):
                os.makedirs(dirTextPath)
            self.storeDocEmbeds(file, original_filename, "TXT")            
            with open(f"{dirTextPath}/{original_filename}.pkl", "rb") as f:
                # Load the vectors from the pickle file
                vectors = pickle.load(f)
        
        return vectors
