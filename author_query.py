# 作者信息查询 
from camel.agents import ChatAgent

from model_base import Deepseek_R1
from search_function import Google_search,Openlibrary_search_author,Wiki_search_author,Get

model = Deepseek_R1()
from model_base import Deepseek_V3
model_=Deepseek_V3()

def Author_query(author_name):
    print("正在进行搜索...")
    
    search_1 = Google_search(author_name,3)  # 查询这个作者在 google 上的信息
    search_2 = Openlibrary_search_author(author_name) # 查询这个作者写的所有书的信息
    search_3 = Wiki_search_author(author_name) # 查询这个作者在 wiki 上的介绍
    system_msg_2 = "你是一个作家校验器，告诉你一个作者的资料，你需要判断这个作家是否真实存在，并且是否政治敏感或反动，如果该作家存在，是一个作家，并且不是中国意义下政治敏感或反动人物，请返回数字\"1\"，否则返回数字\"0\"，注意回答中不能含有冗余信息。"
    chat_agent_2 = ChatAgent(model=model_,system_message=system_msg_2,output_language='zh')
    question_2 = "基本资料：" +author_name +" "
    if len(search_3)>2000:question_2+=search_3[:2000]+" "
    else: question_2+=search_3+" "
    if len(search_1)>6000:question_2+=search_1[:6000]
    else: question_2+=search_1
    response_2 = chat_agent_2.step(question_2)
    content_2=response_2.msgs[0].content
    if content_2=="0":
        print("这并不是一个作家的名字或存在敏感信息，暂时无法回答。")
        return ""
    
    print("正在整理搜索结果...")

    system_msg_1 = "你是一个作家，告诉你一位作者的资料和他写作的书籍，你需要结合作者的写作内容，用相似的风格向读者介绍这位作者，在激起读者对这位作者的兴趣的同时介绍的也要丰富具体，清晰描绘了这位作者基本信息，成就，创作风格，代表作品，生平及影响，可以从文学背景与成长经历，创作理念与思想深度，写作技巧与风格独特性这几个角度介绍。在介绍完后，列出几本最推荐的这位作者的著作，并大致描述每本著作的内容。在最后对和这位作者相关或相似的一些作者进行一些拓展介绍，要时刻注意语言的风格要贴近作者的领域。注意如果出现了在中国意义下的反动或敏感词汇，需要进行屏蔽并抨击。"    
    question_1 = "基本资料：" +author_name +" "+ search_3 + " " + search_1 + "   写作的书籍：" + search_2
    content_1 = Get(model,system_msg_1,'zh',question_1,1)
    if content_1 == "":
        return ""

    return content_1

