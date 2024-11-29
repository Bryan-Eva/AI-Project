import argparse
import time
from datetime import timedelta
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
import numpy as np


DB_FAISS_PATH = "./output_model"
DATA_PATH = "./ApaheTomcatdoc"
def create_vector():
    loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    texts = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L12-v2',
                                       model_kwargs={'device': 'cpu'})
    #embeddings = OllamaEmbeddings(model='llama3')

    db = FAISS.from_documents(texts, embeddings)
    if (not os.path.exists(DB_FAISS_PATH)): os.makedirs(DB_FAISS_PATH)
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    t1 = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default=DATA_PATH)
    parser.add_argument('--faiss', type=str, default=DB_FAISS_PATH)

    config = parser.parse_args()
    if os.path.basename(config.data) not in config.faiss:
        config.fais = os.path.join(config.faiss, os.path.basename(config.data))

    print('訓練開始....\nDATA_PATH={0},\nDB_FAISS_PATH={1}'.format(config.data, config.faiss))

    DATA_PATH = config.data
    DB_FAISS_PATH = config.faiss
    create_vector()
    t2 = time.time()
    td = timedelta(seconds=np.round(t2 - t1, 2))
    print('訓練結束: 耗時 hh:mm:ss: ={0}'.format(td))
    # python Train.py --data C://Users//bryan//Desktop//AI-Python//ApacheTomcatdoc --faiss C://Users//bryan//Desktop//AI-Python//output_model