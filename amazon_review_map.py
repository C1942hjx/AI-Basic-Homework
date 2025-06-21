from langchain_community.document_loaders import CSVLoader

# Amazon 评论数据集 含 640000+ 条书籍评论信息，包括 200000+ 本书籍
# 每本书随机选取至多 5 条评论，附带书籍名称和评分，删去了用户名称等信息

def parse_doc(doc_str):
    result = {}
    # 按行分割并处理每行
    for line in doc_str.split('\n'):
        if ': ' in line:
            parts = line.split(': ', 1)  # 只分割第一个冒号
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            result.setdefault(key, value)
        else:
            # 保留没有冒号的行
            result.setdefault("other_info", []).append(line)
        
    return result

def QueryCSV(bookname,id=0):
    #print("Load")
    loader = CSVLoader('./Amazon 评论数据/processed_books_data'+str(id)+'.csv', encoding='utf-8' )
    docs = loader.load()
    results=[]
    #print("End")
    #print(docs[0])
    for doc in docs :
        parsed = parse_doc(doc.page_content)
        title = parsed.get("Title", "")
        if title==bookname:
            results.append(doc)
    return results

def QueryBook(bookname):
    # 书名查询评论（需要保证在书籍清单内）
    results=[]
    for id in range (0,7):
        temp=QueryCSV(bookname=bookname,id=id)
        for res in temp :
            results.append(res)
    return results
