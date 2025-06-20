# 给定文段查询出自哪本书
from camel.agents import ChatAgent
from model_base import Deepseek_R1,Deepseek_V3
from search_function import Google_search

model = Deepseek_R1()
model1 = Deepseek_V3()

def Text_query(user_question):
    print("正在进行搜索...")
    
    search_1 = Google_search(user_question,5)
    
    print("正在整理搜索结果...")

    system_msg_1 = "你是一个图书检索助手，你需要回答给定的文段来自哪本书籍，保证了文段一定来自某本具体的书的原文，这点很重要，你可以根据给出的章节信息和搜索结果给出最有可能的10本书并分别给出理由。"

    chat_agent_1 = ChatAgent(model=model1,system_message=system_msg_1,output_language='zh')
    question_1 = "用户给的文段：" + user_question + "   网络搜索结果：" + search_1
    response_1 = chat_agent_1.step(question_1)
    content_1=response_1.msgs[0].content


    system_msg_2 = "你是一个审查员，图书检索助手给出了10本和用户给的文段最符合的书并给出了理由，你的目标是按照文段是否原样出现在书籍中将这几本书排序，你需要按照推荐顺序给出这5本书，你不需要给出排除的理由，你只需要给出这5本书和对这5本书推荐的理由，别的任何消息都不要输出。"

    chat_agent_2 = ChatAgent(model=model,system_message=system_msg_2,output_language='zh')
    question_2 = "用户给的文段：" + user_question + "   图书检索助手的回答：" + content_1
    response_2 = chat_agent_2.step(question_2)
    content_2=response_2.msgs[0].content

    return content_2

def Text_query1(user_question,text):
    print("正在进行搜索...")
    
    search_1 = Google_search(user_question,5)
    
    print("正在整理搜索结果...")

    system_msg_1 = "你是一个图书推荐助手，用户给定了书籍信息、参考书籍和网络搜索结果，你需要按照推荐顺序给出10本最符合这些信息的书籍，是否出现原文文段很重要，你可以根据参考书籍和网络搜索结果调整你的答案，输出的书的名字都要用《》括起来，除了按照顺序输出这10本书的名字你不需要输出任何别的信息。"

    chat_agent_1 = ChatAgent(model=model1,system_message=system_msg_1,output_language='zh')
    question_1 = "书籍信息：" + user_question + "\n\n参考书籍：" + text + "\n\n网络搜索结果：" + search_1

#    print(question_1)

    response_1 = chat_agent_1.step(question_1)
    content_1=response_1.msgs[0].content
#    print(content_1)

    return content_1

def Text_query2(user_question):
    system_msg_1 = "你是一个图书检索助手，你需要回答给定的文段来自哪本书籍，保证了文段一定来自某本具体的书的原文，这点很重要，你可以根据给出的章节信息和作者信息给出最有可能的5本书并分别给出理由。"

    chat_agent_1 = ChatAgent(model=model1,system_message=system_msg_1,output_language='zh')
    question_1 = user_question
    response_1 = chat_agent_1.step(question_1)
    content_1=response_1.msgs[0].content
    
    return content_1