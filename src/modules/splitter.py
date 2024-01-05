from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredMarkdownLoader

# Recursive splitting to consider different separators in generic text
r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=200, 
    separators=["\n\n", "\n", " ", ""],
    length_function = len
)

def load_transcript(raw_txt):
    loader = UnstructuredMarkdownLoader(raw_txt)
    
    data = loader.load()
    return data

def split_transcript(raw_txt):
    data = load_transcript(raw_txt)
    print('in split_trans')
    print(data)
    docs = r_splitter.split_documents(data)
    print('docs')
    print(docs)
    return docs