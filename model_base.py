from camel.models import ModelFactory
from camel.types import ModelPlatformType

from dotenv import load_dotenv  
import os  

load_dotenv()

qwen_api_key = os.getenv("QWEN_API_KEY")
qwen_url=os.getenv("QWEN_URL")

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_url=os.getenv("DEEPSEEK_URL")

def Deepseek_R1 ():
    return ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type="deepseek-ai/DeepSeek-R1",
        url=deepseek_url,
        api_key=deepseek_api_key,
        model_config_dict={"max_tokens":16000}
    )

def Deepseek_V3 ():
    return ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type="deepseek-ai/DeepSeek-V3",
        url=deepseek_url,
        api_key=deepseek_api_key,
        model_config_dict={"max_tokens":8000}
    )

def Qwen_72B_Instruct ():
    return ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type="Qwen/Qwen2.5-72B-Instruct",
        url=qwen_url,
        api_key=qwen_api_key,
        model_config_dict={"max_tokens":4000}
    )

def Qwen3_8B ():
    return ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type="Qwen/Qwen3-8B",
        url=qwen_url,
        api_key=qwen_api_key,
        model_config_dict={"max_tokens":8000}
    )