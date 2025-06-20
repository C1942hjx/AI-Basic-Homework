from camel.embeddings import SentenceTransformerEncoder
from camel.retrievers import VectorRetriever
from model_base import Deepseek_R1,Deepseek_V3
from camel.agents import ChatAgent

embedding_model=SentenceTransformerEncoder(model_name='e5-small-v2')

model=Deepseek_R1()
model2=Deepseek_V3()

# 创建并初始化一个向量数据库 (以QdrantStorage为例)
from camel.storages.vectordb_storages import QdrantStorage

vector_storage = QdrantStorage(
    vector_dim=embedding_model.get_output_dim(),
    path="storage_goodreads(2)",
    collection_name="Goodreads 书籍数据集(2)"
)
vr = VectorRetriever(embedding_model= embedding_model,storage=vector_storage)

# Goodreads 数据集2 含 10000 本书籍信息
# 图书元数据： 书名、作者、内容描述，书籍类型
# 包含评分，评分人数信息

def Storagequery(query,top_k=10):
    
    results = vr.query(query=query, top_k=top_k)

    results_string=str(results)

    return results_string

def Goodreads2Search(query,top_k=10):

    #提取关键信息

    print("正在准备...")

    msg1="你是一个书籍推荐助手，给出用户的问题，请提取出关键信息并整理，接下来需要在 Goodreads 向量数据集中进行检索，请用**书籍或作者所在国家的语言**和英语分别输出，同时**不要输出除关键词以外多余的内容干扰向量信息检索**"
    agent1=ChatAgent(model=model,system_message=msg1)
    response1=agent1.step(query)
    res=response1.msgs[0].content

    #向量数据集搜索

    print("正在进行搜索...")

    results_string=Storagequery(res,top_k=top_k)

    #整理搜索结果

    print("正在整理搜索结果...")

    msg2="你是一个书籍推荐助手，给出询问以及在  Goodreads 向量数据集中的检索结果，需要整理检索结果，提取答案，注意过滤掉无用或者错误的信息，避免重复的信息，回答用户"
    question="用户的问题是："+query+" "+"搜搜结果是：" + results_string
    agent2=ChatAgent(model=model2,system_message=msg2,output_language='zh')

    response2 = agent2.step(question)
    return response2.msgs[0].content

