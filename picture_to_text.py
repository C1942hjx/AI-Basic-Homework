# 将图像转成文本
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from paddleocr import PaddleOCR
from model_base import Deepseek_V3,Qwen_72B_Instruct
import numpy as np

model = Qwen_72B_Instruct()
model1 = Deepseek_V3()

def picture_to_text(img):
    agent = ChatAgent(model=model,output_language='zh')

    img_np = np.array(img)
    ocr = PaddleOCR(use_doc_orientation_classify=True,use_doc_unwarping=True,use_textline_orientation=True)
    result = ocr.predict(img_np)
    result_str=str(result)

    system_msg_1 = "你需要把输入的字符串中的有效文字信息拼接成完整的话，尽可能保持原本的文字不要改动。"
    chat_agent_1 = ChatAgent(model=model1,system_message=system_msg_1,output_language='zh')
    question_1 = result_str
    response_1 = chat_agent_1.step(question_1)
    content_1=response_1.msgs[0].content

    user_msg = BaseMessage.make_user_message(role_name="User", content="请简短地描述这张图片的内容", image_list=[img])
    response = agent.step(user_msg)
    answer = '用户文段：' + content_1 + '  助手描述：' + response.msgs[0].content

    system_msg_2 = "这段话里有用户文段和助手描述，你需要根据助手描述修饰用户文段，如果用户文段较为完整就不需要进行修饰，要将编者注的信息删除，尽最大可能保持用户文段的原文"
    chat_agent_2 = ChatAgent(model=model1,system_message=system_msg_2,output_language='zh')
    question_2 = answer
    response_2 = chat_agent_2.step(question_2)
    content_2=response_2.msgs[0].content

    return content_2