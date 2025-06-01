# 将图像转成文本
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from paddleocr import PaddleOCR
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
    chat_agent_1 = ChatAgent(model=model2,system_message=system_msg_1,output_language='zh')
    question_1 = result_str
    response_1 = chat_agent_1.step(question_1)
    content_1=response_1.msgs[0].content
    
    system_msg_3 = "你需要把输入的文段中的错别字纠正，这些错别字都是形近字，输出纠正后的文段，不需要输出你纠正了什么，只要输出纠正后的文段即可。"
    chat_agent_3 = ChatAgent(model=model1,system_message=system_msg_3,output_language='zh')
    question_3 = content_1
    response_3 = chat_agent_3.step(question_1)
    content_3=response_3.msgs[0].content
    
    user_msg = BaseMessage.make_user_message(role_name="User", content="请简短地描述这张图片的内容", image_list=[img])
    agent = ChatAgent(model=model,output_language='zh')
    response = agent.step(user_msg)
    answer = '用户文段：' + content_3 + '  助手描述：' + response.msgs[0].content

    system_msg_2 = "这段话里有用户文段和助手描述，你需要根据助手描述修饰用户文段，如果用户文段比较完整就不需要进行修饰，要检查哪些是编者注释的内容（特别是标注了的引用文章）并全部删除，尽最大可能保持用户文段的原文，可以根据助手描述在末尾添加需要补充的信息。"
    chat_agent_2 = ChatAgent(model=model1,system_message=system_msg_2,output_language='zh')
    question_2 = answer
    response_2 = chat_agent_2.step(question_2)
    content_2=response_2.msgs[0].content

    return content_2