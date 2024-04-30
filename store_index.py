from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain_community.vectorstores import Chroma
# import pinecone
from InstructorEmbedding import INSTRUCTOR

import os

extracted_data = load_pdf("docs/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


direct = 'db'

#Creating Embeddings for Each of The Text Chunks & storing
vectordb = Chroma.from_documents(documents = text_chunks,
                                 embedding = embeddings,
                                 persist_directory = direct)



