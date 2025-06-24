# 一些搜索的函数
from camel.agents import ChatAgent
from model_base import Deepseek_V3
import requests
import os
import json
import wikipedia

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = os.getenv("DEEPSEEK_URL")

model = Deepseek_V3()

def Get(modell,system_msg,output_lan,question,id):
    while True:
        try:
            if output_lan == 'none':
                chat_agent_1 = ChatAgent(model=modell,system_message=system_msg)
            else :
                chat_agent_1 = ChatAgent(model=modell,system_message=system_msg,output_language=output_lan)
            response_1 = chat_agent_1.step(question)
            content_1=response_1.msgs[0].content
            return content_1
        except:
            if id == 1:
                print("调用 Deepseek-R1 API 失败，若需要继续重试请输入 1，若需要退出此次查询请输入 0")
            elif id == 2:
                print("调用 Deepseek-V3 API 失败，若需要继续重试请输入 1，若需要退出此次查询请输入 0")
            else:
                print("调用 Qwen-VL-72B-Instruct 图像模型 API 失败，若需要继续重试请输入 1，若需要退出此次查询请输入 0")
            fl=0
            while True :
                choice = input("请输入选项数字: ").strip()
                if choice == "1":
                    print("正在进行重试...")
                    break
                elif choice == '0':
                    fl=1
                    break
                else :
                    print("无效输入，请重新选择")
            if fl == 1:
                return ""

def Getst(modell, system_msg, output_lan, question, id):
    messages=[]
    from openai import OpenAI
    from openai import APIError, OpenAIError
    if system_msg:
        messages.append({"role": "system", "content": system_msg})
    messages.append({"role": "user", "content": question})
    # output_lan 和 id 在这个版本中同样不直接用于 API 调用
    while True:
        try:
            client = OpenAI(
                base_url=DEEPSEEK_URL,
                api_key=DEEPSEEK_API_KEY,
            )
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=messages,
                stream=True, # 仍然保持流式获取数据，以便可以一块一块地打印
            )
            # 迭代响应并直接打印每个块
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True) # 直接打印内容，并使用 end="" 和 flush=True 实现流式效果
            # 打印一个换行符，以便后续的输出不会紧接着API响应
            print()
            return ""
        except:
            print("调用 Deepseek-V3 API 失败，若需要继续重试请输入 1，若需要退出此次查询请输入 0")
            fl=0
            while True :
                choice = input("请输入选项数字: ").strip()
                if choice == "1":
                    print("正在进行重试...")
                    break
                elif choice == '0':
                    fl=1
                    break
                else :
                    print("无效输入，请重新选择")
            if fl == 1:
                return ""

def Google_search(query, num_results): # google 搜索
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&num={num_results}"
    url_= f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q=\"{query}\"&num={num_results}"
    search_result=' '
    try:
        response = requests.get(url,timeout=5)
        res2=requests.get(url_,timeout=5)
        if response.ok and res2.ok : search_result=response.text+res2.text
        return search_result
    except: 
        print("google API failed")
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