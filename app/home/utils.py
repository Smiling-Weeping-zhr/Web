import instructor
import openai
from pydantic import ValidationError

openai_api_and_url_list = [
    (
        "gpt-4o-mini",
        "sk-fCySjRF5jpYwy2bLc1VaigjTbVQCTWTyjwPJaFOjl5NISO5J",
        "https://xiaoai.plus/v1"
    )
]

def get_openai_key():
    openai_api_and_url = openai_api_and_url_list[0]
    return openai_api_and_url


def get_completion(text=None, retry_total=10):
    """使用自定义API配置获取完成结果"""
    try:
        model, api_key, base_url = get_openai_key()
        
        client = instructor.patch(
            openai.OpenAI(
                api_key=api_key,
                base_url=base_url,
                max_retries=retry_total
            ),
            mode=instructor.Mode.MD_JSON
        )

        article_analysis = client.chat.completions.create(model=model, messages=text)
        return article_analysis.choices[0].message.content
    
    except ValidationError as e:
        for error in e.errors():
            if error['type'] == 'literal_error':
                invalid_value = error['ctx']['input_value']
                print(f"Invalid category value: {invalid_value}")
        raise e
    
    except Exception as e:
        print(f"API请求失败: {str(e)}")
        raise e

def chat_with_ai(user_message, history=None):
    """
    与AI对话 (包含系统提示词 + 历史对话)

    user_message: 当前用户输入
    history: 历史对话列表
    """

    if history is None:
        history = []

    # 系统提示词
    system_prompt = """
You are a helpful AI research assistant.
You help users with:
- datasets
- machine learning
- research papers
- data analysis
- academic questions
Answer clearly and concisely.
"""

    # 构建 messages
    messages = [{"role": "system", "content": system_prompt}]
    # 加入历史对话
    messages.extend(history)

    # 当前用户问题
    messages.append({
        "role": "user",
        "content": user_message
    })

    # 调用你已有的API函数
    reply = get_completion(messages)

    # 更新历史
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    history = history[-6:]
    
    return reply, history