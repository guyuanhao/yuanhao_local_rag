from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()


# 读取已有向量库
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}
)
vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embedding)

# 使用 gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # 或其他Gemini模型
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

query = "请帮我总结这份简历"
print(qa.run(query))
