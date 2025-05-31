# 作者信息查询 
from camel.agents import ChatAgent
from model_base import Deepseek_R1
from search_function import Google_search,Openlibrary_search_author,Wiki_search_author

model = Deepseek_R1

def Author_query(author_name):
    search_1 = Google_search(author_name,5)  # 查询这个作者在 google 上的信息
    search_2 = Openlibrary_search_author(author_name) # 查询这个作者写的所有书的信息
    search_3 = Wiki_search_author(author_name) # 查询这个作者在 wiki 上的介绍

    system_msg_1 = "你是一个作家，告诉你一位作者的资料和他写作的书籍，你需要用诗意的语言向读者介绍这位作者，在激起读者对这位作者的兴趣的同时介绍的也要丰富具体，清晰描绘了这位作者基本信息，成就，创作风格，代表作品，生平及影响。在介绍完后，列出几本最推荐的这位作者的著作，并大致描述每本著作的内容。在最后对和这位作者相关或相似的一些作者进行一些拓展介绍，要时刻注意语言的诗意。"
    chat_agent_1 = ChatAgent(model=model,system_message=system_msg_1,output_language='zh')
    question_1 = "基本资料：" + search_3 + " " + search_1 + "   写作的书籍：" + search_2
    response_1 = chat_agent_1.step(question_1)
    content_1=response_1.msgs[0].content

    return content_1

