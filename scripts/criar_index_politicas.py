from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

import os

with open("data/politicas.md", "r", encoding="utf-8") as f:
    texto = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_text(texto)
documentos = [Document(page_content=doc) for doc in docs]

embeddings = OpenAIEmbeddings()
index = FAISS.from_documents(documentos, embeddings)
index.save_local("data/politicas_index")
print(">>> Índice de políticas salvo com sucesso.")
