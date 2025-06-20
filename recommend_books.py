from camel.agents import ChatAgent
from model_base import Deepseek_R1,Deepseek_V3
from goodreads import GoodreadsSearch
from amazon import AmazonSearch
from amazon_review import AmazonReviewSearch
from text_query import Text_query1,Text_query2

model=Deepseek_V3()
model1=Deepseek_R1()
# 文段查询+信息描述 给10本推荐书籍，从高到低排布 0.5...0.05
# 对于这10本推荐书籍
# 文本匹配上了+0.3
# 作者正确+0.2
def Recommend_books(criteria):
#    搜索书籍在库里的匹配信息，选出一部分作为参考书籍
    search_2=""
    search_3=""
    search_4=""
    search_4 = Text_query2(str(criteria))
    print(search_4)
    search_2 = GoodreadsSearch(str(criteria),3)
    search_3 = AmazonSearch(str(criteria),3)
    text = search_4 + "\n" + search_2 + "\n" + search_3
    search_1 = Text_query1(str(criteria),text)
    lenn = len(search_1)
    ls=cnt=0
    lst=[]
    text1=""
    my_map={}
    for i in range(0,lenn):
        if search_1[i] == "《":
            ls=i
        elif search_1[i] == "》":
            tmp="《"
            for j in range(ls+1,i):
                tmp=tmp+search_1[j]
            tmp=tmp+"》"
            my_map[tmp]=cnt
            cnt=cnt+1
            text1=text1+tmp+"  "
            lst.append(tmp)
#    print(search_1)
#    print(lst)
    lenn1=len(lst)
#    print(lenn1)
    score=[]
    for i in range(0,lenn1):
        sc=0.5*(1.0-(float)(i)/(10.0))
        score.append(sc)
    
    # 作者是否正确 +0.2
    msg1="给定作者和你需要判断的书籍，你需要对每一本书判断这位作者是不是大概率写过这本书，如果写过就输出这本书的名字，最后你只需要输出这位作者写过的在需要判断的书籍里的书的名字，输出的书的名字都要用《》括起来，别的信息全都不要输出"
    agent1=ChatAgent(model=model,system_message=msg1)
    query = "作者：" + criteria["author"] + "\n需要判断的书籍：" + text1
    response1=agent1.step(query)
    res=response1.msgs[0].content

    lenn = len(res)
    for i in range(0,lenn):
        if res[i] == "《":
            ls=i
        elif res[i] == "》":
            tmp="《"
            for j in range(ls+1,i):
                tmp=tmp+res[j]
            tmp=tmp+"》"
            score[my_map[tmp]]+=0.2
    
    #   文本是否出现 +0.3
    msg2="给定文本和你需要判断的书籍，你需要对每一本书判断这段文本是不是大概率出现在这本书，如果这段文本在这本书中出现了就输出这本书的名字，最后你只需要输出在需要判断的书籍里并且出现了这段文本的书的名字，输出的书的名字都要用《》括起来，别的信息全都不要输出"
    agent2=ChatAgent(model=model,system_message=msg2)
    query = "文本：" + criteria["text"] + "\n需要判断的书籍：" + text1
    response2=agent2.step(query)
    res=response2.msgs[0].content

    lenn = len(res)
    ls=0
    for i in range(0,lenn):
        if res[i] == "《":
            ls=i
        elif res[i] == "》":
            tmp="《"
            for j in range(ls+1,i):
                tmp=tmp+res[j]
            tmp=tmp+"》"
            score[my_map[tmp]]+=0.3
    text2=""
    for i in range(0,lenn1):
        text2 = text2 + (str)(lst[i]) + ": " + (str)(score[i])+"\n"
    print(text2)
    msg3="你是书籍推荐员，给定参考推荐书籍和这些书籍的评分，你需要在推荐书籍的基础上根据书籍描述按照推荐顺序给出5本推荐书籍和理由，你只需要按照顺序输出这些书和理由，别的信息全都不要输出"
    agent3=ChatAgent(model=model,system_message=msg3)
    query = "参考推荐书籍及评分："+ text2 + "\n书籍描述："+ str(criteria)
    response3 = agent3.step(query)
    res = response3.msgs[0].content
    
    msg4="你是书籍推荐员，给定5本书，你需要根据书籍描述为这5本书编撰推荐理由，你只需要输出这5本书和他们的推荐理由，理由里面不应该包含评分，而更应该围绕书籍描述展开，别的信息全都不要输出"
    agent4=ChatAgent(model=model,system_message=msg4)
    query = "5本书："+ res + "\n书籍描述："+ str(criteria)
    response4 = agent4.step(query)
    
    return response4.msgs[0].content