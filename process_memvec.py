from model_base import Deepseek_V3
from search_function import Get
from camel.memories.records import MemoryRecord
from camel.messages import BaseMessage
from camel.types import OpenAIBackendRole

model=Deepseek_V3()

def extract_memvec(content):
    msg0="给出5本书，并且每本书会给出一个对应的理由，你需要完全忽略每本书对应的理由，这是完全无关的信息，你只需要关注这五本书。你需要对每一本书简述其题材、风格和作者，对于每一本书输出一行表示对应的尽量简洁的简述，不需要输出编号，只需要输出简述，其他的信息都不需要输出。"
    query = "给出的5本书：" + content
    res=Get(model,msg0,'none',query,2)
    # print(res)
    res=res+"\n"
    lenn = len(res)
    ls=0
    ret=[]
    for i in range(0,lenn):
        if res[i] == "\n":
            tmp=""
            for j in range(ls,i):
                tmp=tmp+res[j]
            ls=i+1
            # print(tmp)
            if len(tmp) > 5:
                ret.append(MemoryRecord(
                    message=BaseMessage.make_assistant_message(role_name="assistant", content=tmp),
                    role_at_backend=OpenAIBackendRole.ASSISTANT
                    ),
                )
            # print("one whole line above")
    return ret

def author_memvec(author):
    msg0="给定一位作家，你需要简述这位作家的题材和风格，只需要输出尽量简洁的简述，只输出一行，简述中不应该包含作家的名字，其他的信息都不需要输出。"
    query = "给出的作家：" + author
    res=Get(model,msg0,'none',query,2)
    # print("dbgflag-author_memvec:")
    # print(res)
    # print("dbgflag-author_memvec ends")
    ret=[]
    if res != "":
        res=author+"，"+res
        # print(res)
        ret.append(MemoryRecord(
            message=BaseMessage.make_assistant_message(role_name="assistant", content=res),
            role_at_backend=OpenAIBackendRole.ASSISTANT
            )
        )
    return ret

# author_memvec("阿西莫夫")