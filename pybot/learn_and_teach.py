import openai
import os
from langchain.llms import OpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain






############# train the language model with finance concepts ############
# urls = [
#     "https://en.wikipedia.org/wiki/Capital_asset_pricing_model",
# ]
# loaders = UnstructuredURLLoader(urls=urls)
# data = loaders.load()
# text_splitter = CharacterTextSplitter(
#     separator='\n',
#     chunk_size=1000,
#     chunk_overlap=200
# )
# docs = text_splitter.split_documents(data)

# embeddings = OpenAIEmbeddings()
# vectorStore_openAI = FAISS.from_documents(docs, embeddings)
# with open("faiss_store_openai.pk1", "wb") as f:
#     pickle.dump(vectorStore_openAI, f)


##################### get finance info #######################
def teach_information(concept, chat):
    with open("faiss_store_openai.pk1", "rb") as f:     
        VectorStore = pickle.load(f)
        chain = RetrievalQAWithSourcesChain.from_llm(llm = chat, retriever = VectorStore.as_retriever())
        print(chain({"question":f'explain {concept} like im 5 years old'}, return_only_outputs=True))
