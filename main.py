import logging
logging.getLogger("torch.distributed.elastic.multiprocessing").setLevel(logging.ERROR)

from PIL import Image
from picture_to_text import Picture_to_text
from text_query import Text_query
from author_query import Author_query
from recommend_books import Recommend_books

from camel.memories.blocks.vectordb_block import VectorDBBlock
from camel.embeddings import SentenceTransformerEncoder
vector_db_block = VectorDBBlock(embedding=SentenceTransformerEncoder(model_name='e5-small-v2'))
from process_memvec import extract_memvec,author_memvec

print("\n您好，我是一个 📚 书籍推荐助手 📚 \n")

while True:
    print("\n请选择功能：")
    print("1. 通过文段/图片查书")
    print("2. 查询作家信息")
    print("3. 智能书籍推荐")
    print("0. 退出")
    
    choice = input("请输入选项数字: ").strip()
    
    if choice == "1":
        # 文段查书功能
        input_type = input("输入类型 [1:文本 / 2:图片]: ").strip()
        fl=1
        if input_type == "1":
            text = input("请输入文段: ")
        elif input_type == "2":
            img_path = input("请输入图片路径: ")
            try:
                text = Picture_to_text(img_path)
            except:
                text=' '
                fl=0
        else : fl=2
        
        if fl == 0 :
            print("图片解析失败")
        elif fl == 2 :
            print("无效输入，请重新选择")
        else :
            books = Text_query(text)
            if books != "":
                vector_db_block.write_records(extract_memvec(books))
            
            # print("dbgflag-stretval")
            # print(books)
            # keyword = "北京折叠"
            # retrieved_records = vector_db_block.retrieve(keyword=keyword, limit=8)
            # for record in retrieved_records:
            #     print(f"UUID: {record.memory_record.uuid}, Message: {record.memory_record.message.content}, Score: {record.score}")
    
    elif choice == "2":
        # 作家查询功能
        author = input("请输入作家姓名: ")
        info = Author_query(author)
        if info != "":
            vector_db_block.write_records(author_memvec(author))

        # print("dbgflag-stretval")
        # print(info)
    
    elif choice == "3":
        # 智能推荐功能
        print("\n请提供推荐依据(按Enter跳过):")
        criteria = {
            "text": input("相关文段: "),
            "author": input("偏爱作者: "),
            "purpose": input("其它描述（体裁偏好/内容描绘/阅读目的）: ")
        }
        Recommend_books(criteria,vector_db_block)
    elif choice == "0":
        break
    else:
        print("无效输入，请重新选择")