import os
from typing import List
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class RAGEngine:
    def __init__(self, data_dir: str = "data", persist_dir: str = "chroma_db"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
        self.vector_store = None
        self.qa_chain = None

    def ingest_documents(self):
        """Load, split, and index documents."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        loader = DirectoryLoader(self.data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        
        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        print(f"Ingested {len(texts)} chunks from {len(documents)} documents.")

    def load_vector_store(self):
        """Load existing vector store."""
        self.vector_store = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )

    def setup_qa_chain(self):
        """Initialize the RetrievalQA chain."""
        if not self.vector_store:
            self.load_vector_store()
            
        prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer:"""
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

    def query(self, question: str):
        """Execute a query against the RAG pipeline."""
        if not self.qa_chain:
            self.setup_qa_chain()
        return self.qa_chain.invoke({"query": question})
