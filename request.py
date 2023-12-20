import requests
from translate import Translator

msg_history=[
    {"role": "system", "content": "You are a helpful AI assistant"},
]
url = "http://0.0.0.0:8080/v1/chat/completions"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
data = {
    "messages": msg_history,
    "model": "tinyllama-1"
}

def send_post_request(question):
    # 发送 POST 请求
    eng=Translator(from_lang="ZH",to_lang="EN-US").translate(question)                
    msg_history.append({"role":"user","content":"Answer briefly,not more than 500 chars:"+eng})
    response = requests.post(url, headers=headers, json=data)

    response.raise_for_status()
    response_data = response.json()
    
    try:
        msg=response_data['choices'][0]["message"]['content']
    except:
        msg=None
    # 返回接收到的数据
    return msg

# 调用封装的函数

