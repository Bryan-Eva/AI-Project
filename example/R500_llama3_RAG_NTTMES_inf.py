####################################################################################
#  source code from: ITRI_EOSL R5_llama3 Test @rachelliu
#
#  reference from github:  https://github.com/R300-AI/ITRI_Ollama_RAG.git
#
#
#  pip install Ollama  langchain langchain_openai rich
#  Ollama run llama3, phi3, llama2, mistral
#  FY112_GPT310--------code
#  ssh rachelliu@140.96.98.113
#  conda activate FY112_GPT310
#  cd 2024_llama3
#  python R500_llama3_RAG_NTTMES_inf.py
#  python R500_llama3_RAG_NTTMES_inf.py --gpt phi3
####################################################################################

import os
from langchain_community.llms import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
import argparse
import shutil
import configparser
from datetime import timedelta
import time
import numpy as np
import math
import datetime
from datetime import datetime
import random
import string
import os

from transformers.models.cvt.convert_cvt_original_pytorch_checkpoint_to_pytorch import embeddings


def setinfo(c_logPath='r500.txt',type='info',text=''):
    tt2 = str(datetime.now().strftime("%Y%m%d_%H:%M:%S.%f")) #取到秒鐘
    #print("{:20s}|{:>16s}|{}".format(tt2,str(type).upper(),text))
    with open(c_logPath, 'a+', encoding='utf-8') as f: #, encoding='utf-8'
        f.write("{:20s}|{:>16s}|{}\n".format(tt2,str(type).upper(),text))
def genguidtxt():
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d-%H-%M")
    random_number = random.randint(100000, 999999)
    # 生成四位數字
    digits = ''.join(random.choices(string.digits, k=4))

    # 生成兩位字母
    letters = ''.join(random.choices(string.ascii_letters, k=2))

    # 將數字和字母混合打亂
    random_str = ''.join(random.sample(digits + letters, 6))

    # 组合時間+亂數
    result = f"{time_str}-{random_str}.txt"
    #print(result)
    return result
# 初始化Ollama模型
# 創建文件鏈，將llm和提示模板結合
def prompt_template():
    # 設定提示模板，將系統和使用者的提示組合
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Answer the user\'s questions in Chinese, based on the context provided below:\n\n{context} '),
        ('user', 'Question: {input} #zh-tw'),
    ])
    return prompt

def load_trained_db(DB_FAISS_PATH="../output_model"):
    embeddings =  HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L12-v2',
                                        model_kwargs={'device': 'cpu'})
    #embeddings = OllamaEmbeddings()
    try:
        vectordb = FAISS.load_local(DB_FAISS_PATH, embeddings,allow_dangerous_deserialization=True)
        # 將向量資料庫設為檢索器
        retriever = vectordb.as_retriever()
    except FileNotFoundError:
        print(f"{DB_FAISS_PATH} 的數據路徑錯誤")
        return 0,'Err001'
    except Exception as e:
        print(f"{e}讀取db錯誤")
        return 0,f'Err002-{e}'
    return 1,retriever
def main(config):
    prompt=prompt_template()
    llm = Ollama(model=config.gpt)
    document_chain = create_stuff_documents_chain(llm, prompt)
    f,retriever=load_trained_db(DB_FAISS_PATH=config.m)
    if(config.islog):
        if(not os.path.exists(config.logpath)): os.mkdir(config.logpath)
        txtfile = genguidtxt()
        c_logPath = os.path.join(config.logpath, txtfile)
        setinfo(c_logPath=c_logPath,text='initialized...config={0}'.format(config))

    # 創建檢索鏈，將檢索器和文件鏈結合
    if(f==1):
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        context = ['Assuming you are an expert in smart factory, software and operations communications']
        input_text = input('>>> 請提問... (輸入 -1 表示結束)\n')
        index = 1
        while input_text.lower() != '-1':
            t1=time.time()
            response = retrieval_chain.invoke({
                'input': input_text,
                'context': context
            })
            ans = response['answer']
            doc = response['context']
            ###################################
            #把response給print出來~
            ###################################
            print(ans)

            if(config.isref): print(doc)
            t2=time.time()
            td = timedelta(seconds=np.round(t2-t1,2))
            print(f'第{index}次訪問結束: 耗時 hh:mm:ss:fff ={td}')
            if(config.islog):
                setinfo(c_logPath=c_logPath,type='Q',text=f'{index:03}-{input_text}')
                setinfo(c_logPath=c_logPath,type='A',text=f'{index:03}-{ans}')
                if(config.isref):
                    setinfo(c_logPath=c_logPath,type='doc',text=f'{index:03}-{doc}')
                setinfo(c_logPath=c_logPath,type='time',text=f'{index:03}-{td}')

            input_text = input('>>> 請提問... (輸入-1表示結束)\n')
            index +=1
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--m', type=str, default="../output_model")
    parser.add_argument('--gpt', type=str, default='llama3', choices=['llama3', 'llama2', 'phi3', 'mistral'])
    parser.add_argument('--isref', type=int, default=0, choices=[0,1])
    parser.add_argument('--islog', type=int, default=1, choices=[0,1])
    parser.add_argument('--logpath', type=str, default=r"../log")
    config = parser.parse_args()
    main(config)
