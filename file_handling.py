from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# 加载文档
loader = PyPDFLoader("docs/cv.pdf")
docs = loader.load()

# 切分文本
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs_split = splitter.split_documents(docs)

# 向量化
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}
)

# 存储到本地 Chroma
vectordb = Chroma.from_documents(docs_split, embedding, persist_directory="./chroma_db")
vectordb.persist()