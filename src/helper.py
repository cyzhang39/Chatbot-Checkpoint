from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()


#Extract data from the PDF
def load_pdf(data):
    loader = DirectoryLoader('docs/', glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    return documents



#Create text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks



#download embedding model
def download_hugging_face_embeddings():
    model = "BAAI/bge-large-zh"
    embeddings = HuggingFaceEmbeddings(model_name=model)
    print(model)
    return embeddings