# 给定文段查询出自哪本书
from camel.agents import ChatAgent
from model_base import Deepseek_R1
from search_function import Google_search

model = Deepseek_R1()

def Text_query(user_question):
    user_question = input()

    search_1 = Google_search(user_question,5)

    system_msg_1 = "你是一个图书检索助手，你需要回答给定的文段来自哪本书籍，保证了文段一定来自某本具体的书的原文，这点很重要，你可以根据给出的章节信息和搜索结果给出最有可能的5本书并分别给出理由。"
    chat_agent_1 = ChatAgent(model=model,system_message=system_msg_1,output_language='zh')
    question_1 = "用户给的文段：" + user_question + "   网络搜索结果：" + search_1
    response_1 = chat_agent_1.step(question_1)
    content_1=response_1.msgs[0].content

    system_msg_2 = "你是一个审查员，图书检索助手给出了5本和用户给的文段最符合的书并给出了理由，你的目标是按照文段是否原样出现在书籍中将这几本书排序，你需要按照推荐顺序给出这5本书。"
    chat_agent_2 = ChatAgent(model=model,system_message=system_msg_2,output_language='zh')
    question_2 = "用户给的文段：" + user_question + "   图书检索助手的回答：" + content_1
    response_2 = chat_agent_2.step(question_2)
    content_2=response_2.msgs[0].content

    return content_2

