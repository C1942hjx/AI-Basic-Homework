# 将图像转成文本
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from paddleocr import PaddleOCR
from search_function import Get

from model_base import Deepseek_V3,Deepseek_R1,Qwen_VL_72B_Instruct
from PIL import Image
import numpy as np
import subprocess
import sys
from pathlib import Path

model = Qwen_VL_72B_Instruct()
model1 = Deepseek_R1()
model2 = Deepseek_V3()

def Picture_to_text(img_path_):
    print("正在将图片转为文字...")
    
    img_path = str(Path(img_path_))
    img = Image.open(img_path)
    img_np = np.array(img)
    
    def silent_paddleocr(image_path):
        cmd = [
            sys.executable, "-c",
            f"""
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
ocr = PaddleOCR()
image = Image.open(r"{image_path}")
image_np = np.array(image)
result = ocr.predict(image_np)
print(str(result))
            """
        ]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="gbk",
            errors="ignore"
        )
        return result.stdout.strip()

    result_str= silent_paddleocr(img_path_)

    # ocr = PaddleOCR()
    # result = ocr.predict(img_np)
    # result_str=str(result)

    system_msg_1 = "你需要把输入的字符串中的有效文字信息拼接成完整的话，尽可能保持原本的文字不要改动，你只需要输出这一段话即可。"
    question_1 = result_str
    content_1 = Get(model2,system_msg_1,'zh',question_1,2)
    if content_1 == "":
        return ""
    
    system_msg_3 = "你需要把输入的文段中的错别字纠正，这些错别字都是形近字，输出纠正后的文段，不需要输出你纠正了什么，只要输出纠正后的文段即可。"
    question_3 = content_1
    content_3 = Get(model2,system_msg_3,'zh',question_3,2)
    if content_3 == "":
        return ""

    user_msg = BaseMessage.make_user_message(role_name="User", content="请简短地描述这张图片的内容", image_list=[img])
    while True:
        try:
            agent = ChatAgent(model=model,output_language='zh')
            response = agent.step(user_msg)
            res = response.msgs[0].content
            break
        except:
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
                res = ""
                break
    if res == "":
        return ""
    answer = '用户文段：' + content_3 + '  助手描述：' + res

    system_msg_2 = "这段话里有用户文段和助手描述，你需要根据助手描述修饰用户文段，如果用户文段比较完整就不需要进行修饰，要检查哪些是编者注释的内容（特别是标注了的引用文章）并全部删除，尽最大可能保持用户文段的原文，可以根据助手描述在末尾添加需要补充的信息。"
    question_2 = answer
    content_2 = Get(model2,system_msg_2,'zh',question_2,2)
    if content_2 == "":
        return ""

    return content_2