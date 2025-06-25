from camel.agents import ChatAgent
from model_base import Deepseek_R1,Deepseek_V3
from goodreads import GoodreadsSearch
from goodreads2 import Goodreads2Search
from amazon import AmazonSearch
from amazon_review import AmazonReviewSearch
from text_query import Text_query1,Text_query2
from search_function import Get,Getst

model=Deepseek_V3()
model1=Deepseek_R1()
# 文段查询+信息描述 给10本推荐书籍，从高到低排布 0.5...0.05
# 对于这10本推荐书籍
# 文本匹配上了+0.3
# 作者正确+0.2
def Recommend_books(criteria,vector_db_block):
#    搜索书籍在库里的匹配信息，选出一部分作为参考书籍
    search_2=""
    search_3=""
    search_4=""
    search_4 = Text_query2(str(criteria))
    search_2 = Goodreads2Search(str(criteria),3)
    search_3 = AmazonSearch(str(criteria),3)
    text = search_4 + "\n" + search_2 + "\n" + search_3
    search_1 = Text_query1(str(criteria),text)

    system_msg_5 = "你是一个敏感词屏蔽器，告诉你用户提供的信息和网络搜索结果，你需要判断这些内容是否是无意义内容或属于敏感内容，如果不是无意义内容也不属于中国意义下的敏感或反动，返回数字\"1\"，否则返回数字\"0\"，注意回答中除了数字1或0不能含有任何冗余信息。"
    question_5 = "用户提供的信息：" +str(criteria) + "\n搜索结果：" + search_1
    content_5=Get(model,system_msg_5,'zh',question_5,2)
    if content_5 == "":
        return ""
    if content_5=="0":
        print("您的输入是无意义内容或存在敏感信息，暂时无法回答。")
        return ""
    
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
    lenn1=len(lst)
    score=[]
    for i in range(0,lenn1):
        sc=0.5*(1.0-(float)(i)/(10.0))
        score.append(sc)
    
    # print("dbgflag-namelist:")
    # print(text1)

    msg0="按顺序给定一些书籍，你需要按输入顺序对每一本书简述其题材、风格和作者，对于每一本书输出一行表示对应的尽量简洁的简述，但必须包含前文所述的三个要素，不需要输出编号，只需要输出简述，其他的信息都不需要输出"
    query = "给定的书籍：" + text1
    res=Get(model,msg0,'none',query,2)
    if res == "":
        return ""
    # print("dbgflag-summary:")
    # print(res)
    # print("try-formatting:")

    res=res+"\n"
    lenn = len(res)
    ls=0
    idx=0
    for i in range(0,lenn):
        if res[i] == "\n":
            tmp=""
            for j in range(ls,i):
                tmp=tmp+res[j]
            ls=i+1
            # print(tmp)
            retrieved_records = vector_db_block.retrieve(keyword=tmp, limit=3)
            coef=10.0
            dbg_del=0
            for record in retrieved_records:
                # print(f"UUID: {record.memory_record.uuid}, Message: {record.memory_record.message.content}, Score: {record.score}")
                score[idx]+=record.score*coef
                dbg_del+=record.score*coef
                coef*=0.7
            idx+=1
            # print("dbg_scoredel:")
            # print(dbg_del)
            # print("one whole line above")

    # text2=""
    # for i in range(0,lenn1):
    #     text2 = text2 + (str)(lst[i]) + ": " + (str)(score[i])+"\n"

    # 作者是否正确 +0.2
    msg1="给定作者和你需要判断的书籍，你需要对每一本书判断这位作者是不是大概率写过这本书，如果写过就输出这本书的名字，最后你只需要输出这位作者写过的在需要判断的书籍里的书的名字，输出的书的名字都要用《》括起来，别的信息全都不要输出"
    query = "作者：" + criteria["author"] + "\n需要判断的书籍：" + text1
    res=Get(model,msg1,'none',query,2)
    if res == "":
        return ""

    # print("dbgflag-author:")
    # print(res)
    # print("dbgflag-author ends")

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
    query = "文本：" + criteria["text"] + "\n需要判断的书籍：" + text1
    res=Get(model,msg2,'none',query,2)
    if res == "":
        return ""

    # print("dbgflag-extract:")
    # print(res)
    # print("dbgflag-extract ends")

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

    # print(text2)

    msg3="你是书籍推荐员，给定参考推荐书籍和这些书籍的评分，你需要在推荐书籍的基础上根据书籍描述按照推荐顺序给出5本推荐书籍和理由，你只需要按照顺序输出这些书和理由，别的信息全都不要输出"
    query = "参考推荐书籍及评分："+ text2 + "\n书籍描述："+ str(criteria)
    res=Get(model,msg3,'none',query,2)
    if res == "":
        return ""
    
    msg4="你是书籍推荐员，给定5本书，你需要根据书籍描述为这5本书编撰推荐理由，你只需要输出这5本书和他们的推荐理由，理由里面不应该包含评分，而更应该围绕书籍描述展开，别的信息全都不要输出"
    query = "5本书："+ res + "\n书籍描述："+ str(criteria)
    Getst(model,msg4,'none',query,2)