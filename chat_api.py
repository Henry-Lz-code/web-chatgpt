# -*- coding: UTF-8 -*-

import openai

from config import settings

openai.api_key = settings["gpt_api_key"]
openai.api_base = settings["basePath"]
# openai.proxy = settings["proxy"]


def request_chatgpt(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        stream=True
    )
    return response


if __name__ == '__main__':
    msg_list = [
        {
            'role': 'user',
            'content': 'who are you?'
        }
    ]
    iter_res = request_chatgpt(msg_list)
    chunk_messages = []
    for msg in iter_res:
        delta = msg['choices'][0]['delta']
        chunk_messages.append(delta)
        print(delta)
    print(f"GPT: {''.join([m.get('content', '') for m in chunk_messages])}")
