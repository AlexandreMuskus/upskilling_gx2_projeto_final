import os
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

# Embeddings e FAISS
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
# Caminhos
INDEX_PATH = "data/vector_index"
CATALOGO_PATH = "data/produtos.json"

def carregar_dados():
    docs = []

    # Carregar políticas
    with open("data/politicas.md", "r", encoding="utf-8") as f:
        texto = f.read()
        docs.append(Document(page_content=texto, metadata={"origem": "politicas"}))

    # Carregar produtos
    with open("data/produtos.json", "r", encoding="utf-8") as f:
        produtos = json.load(f)
        for produto in produtos:
            texto = f"{produto['nome']}: {produto['descricao']} - Especificações: {produto['especificacoes']}"
            docs.append(Document(page_content=texto, metadata={"origem": "produto", "id": produto["id"]}))

    return docs

def construir_index():
    docs = carregar_dados()
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    textos = splitter.split_documents(docs)
    db = FAISS.from_documents(textos, embeddings)
    db.save_local(INDEX_PATH)

def buscar_conhecimento(pergunta: str, k: int = 3) -> str:
    db = FAISS.load_local(INDEX_PATH, embeddings)
    resultados = db.similarity_search(pergunta, k=k)
    return "\n".join([doc.page_content for doc in resultados])

# Carrega o índice FAISS
def carregar_index():
    print(">>> Carregando índice FAISS...")
    embeddings = OpenAIEmbeddings()
    index = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    print(">>> Índice carregado com sucesso!")
    return index

# Busca produtos com base em uma consulta semântica
def buscar_produto(consulta: str, k: int = 5):
    index = carregar_index()
    resultados = index.similarity_search(consulta, k=k)

    if not resultados:
        return []

    # Lê o catálogo
    with open(CATALOGO_PATH, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    # Busca por nome do produto dentro dos documentos retornados
    produtos_encontrados = []
    for r in resultados:
        texto = r.page_content.lower()
        for produto in catalogo:
            nome = produto["nome"].lower()
            if nome in texto:
                produtos_encontrados.append(produto)
                break

    return produtos_encontrados

def buscar_politica(pergunta: str, k: int = 3):
    embeddings = OpenAIEmbeddings()
    index = FAISS.load_local("data/politicas_index", embeddings, allow_dangerous_deserialization=True)
    resultados = index.similarity_search(pergunta, k=k)
    return [r.page_content for r in resultados]

