# RUN: python3 ingest.py

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import argparse
import shutil
import configparser
import os
from datetime import datetime
import numpy as np
import time
from datetime import timedelta
#DATA_PATH = r"D:/R500-A30335/train_input_data/20240409_test_data"
DATA_PATH = "../pdf"
#DB_FAISS_PATH = os.path.join(r"D:/R500-A30335/train_output_FAISS", os.path.basename(DATA_PATH))
DB_FAISS_PATH = "../train_output_FAISS"

# Create vector database
def create_vector_db():
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    if(not os.path.exists(DB_FAISS_PATH)): os.makedirs(DB_FAISS_PATH)
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    
    t1=time.time()
    parser=argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default=DATA_PATH)
    parser.add_argument('--faiss', type=str, default=DB_FAISS_PATH)

    #--data /home/hduser/Desktop/chainlit/trainData/EDA+DSO+DSE
    #--faiss /home/hduser/Desktop/chainlit/DSOV1
    config = parser.parse_args()
    if(os.path.basename(config.data) not in config.faiss):
        config.faiss = os.path.join(config.faiss, os.path.basename(config.data))
    print('訓練開始....\nDATA_PATH={0},\nDB_FAISS_PATH={1}'.format(config.data, config.faiss))
    
    
    DATA_PATH=config.data
    DB_FAISS_PATH=config.faiss
    create_vector_db()
    t2=time.time()
    td = timedelta(seconds=np.round(t2-t1,2))
    print('訓練結束: 耗時 hh:mm:ss: ={0}'.format(td))
    #python EOSLR500_train_ingest.py --data /home/hduser/Desktop/chainlit/trainData/EDA+DSO+DSE --faiss /home/hduser/Desktop/chainlit/DSOV1
