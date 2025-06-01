# 一些搜索的函数
from camel.agents import ChatAgent
from model_base import Deepseek_V3
import requests
import os
import wikipedia

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
model = Deepseek_V3()

def Google_search(query, num_results): # google 搜索
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&num={num_results}"
    search_result=' '
    try:
        response = requests.get(url,timeout=5)
        if response.ok : search_result =response.text
        return search_result
    except:
        return search_result

def Wiki_search_author(author_name): # 维基百科搜索作者
    wikipedia.set_lang("zh")
    try:
        search_results = wikipedia.search(author_name)
        List = str(search_results)
    
        system_msg_search = "你是一个搜索助手，给了你用户要找的作者和一个列表，如果所有列表中的元素都不是这个作者，那么返回一个字空，要特别严格的判断每个元素是不是用户给定的作者，否则你需要回答这个列表里哪个搜索结果是这个作者，你只需要回答一个列表中的元素即可，不要说别的任何话。如果最后输出的结果并不是一个作家，请也返回一个字空。"
        chat_agent = ChatAgent(system_message=system_msg_search,model=model,output_language='zh',)

        question = "用户要找的作者："+author_name + "    列表：" + List
        response = chat_agent.step(question)
        content = response.msgs[0].content
        search = search_ = ' '

        try:
            page = wikipedia.page(content)
            search_ = page.content
        except :
            search_ = ' '

        if len(search_)>10000 : search = search_[:10000]
        else : search = search_
        return search
    except :
        return " "

def Openlibrary_search_author(author_name): # openlibrary 搜索作者写的书籍
    url = f"https://openlibrary.org/search.json?author={author_name}"
    try:
        response = requests.get(url,timeout=5)
        data = response.json()
        books = []
        for book in data.get("docs", []):
           title = book.get("title", "无标题")
           publish_year = book.get("first_publish_year", "未知")
           books.append({
             "title": title,
             "published_date": publish_year
          })
        return str(books)
    except:
        return " "