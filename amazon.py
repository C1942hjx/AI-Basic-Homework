from camel.embeddings import SentenceTransformerEncoder
from camel.retrievers import VectorRetriever
from model_base import Deepseek_R1,Deepseek_V3
from camel.agents import ChatAgent

embedding_model=SentenceTransformerEncoder(model_name='e5-small-v2')

model=Deepseek_R1()
model2=Deepseek_V3()

# 创建并初始化一个向量数据库 (以QdrantStorage为例)
from camel.storages.vectordb_storages import QdrantStorage

# Amazon 数据集 含 210000+ 本书籍信息
# 图书元数据： 书名、作者、出版社、出版日期、书籍描述、书籍类别

def VectorSearch(query,top_k=10,id=0):
    
    vector_storage = QdrantStorage(
        vector_dim=embedding_model.get_output_dim(),
        path="storage_amazon",
        collection_name="Amazon 图书元数据"+str(id)
    )
    vr = VectorRetriever(embedding_model= embedding_model,storage=vector_storage)
    
    results = vr.query(query=query, top_k=top_k)

    return results

def Storagequery(query,top_k=10):
    
    results=VectorSearch(query,top_k=top_k,id=0)

    for id in range(1,12):
        results2=VectorSearch(query,top_k=top_k,id=id)
        for i in range(0,top_k) :
            if results2[i]["similarity score"] > results[top_k-1]["similarity score"] :
                results[top_k-1]=results2[i]
                for j in range(top_k-1,0,-1):
                    if results[j]["similarity score"] > results[j-1]["similarity score"] :
                        tmp =results[j]
                        results[j]=results[j-1]
                        results[j-1]=tmp
                    else :
                        break

    results_string=str(results)
    
    return results_string

def AmazonSearch(query,top_k=10):

    #提取关键信息

    print("正在准备...")

    msg1="你是一个书籍推荐助手，给出用户的问题，请提取出关键信息并整理，注意书籍名称、书籍特征、书籍类别等信息，接下来需要在 Amazon 向量数据集中进行检索，请用**书籍或作者所在国家的语言**和英语分别输出，同时**不要输出除关键词以外多余的内容干扰向量信息检索**"
    agent1=ChatAgent(model=model,system_message=msg1)
    response1=agent1.step(query)
    res=response1.msgs[0].content

    #向量数据集搜索

    print("正在进行搜索，由于数据较多，这可能需要一些时间...")

    results_string=Storagequery(res,top_k=top_k)
    
    #整理搜索结果

    print("正在整理搜索结果...")

    msg2="你是一个书籍推荐助手，给出询问以及在 Amazon 向量数据集中的检索结果，需要整理检索结果，提取答案，注意过滤掉无用或者错误的信息，避免重复的信息，回答用户"
    question="用户的问题是："+query+" "+"搜搜结果是：" + results_string
    agent2=ChatAgent(model=model2,system_message=msg2,output_language='zh')

    response2 = agent2.step(question)
    return response2.msgs[0].content

