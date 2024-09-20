"""
This is the file that contains OpenAI API related constants.
Also this checks the version of the OpenAI package and raises an exception if the version is below 1.0.
"""

import base64
import os.path
#import httpx
import openai
from openai import OpenAI
import logging

from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.models import ChatMessageContainer
from pyqt_openai.sqlite import SqliteDatabase

DB = SqliteDatabase()

# initialize

# Настройка логирования
# logging.basicConfig(
#     level = logging.DEBUG, # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     filename = '/tmp/openai.log',  # Путь к файлу логов
#     filemode = 'a' # Режим записи (a - append, w - write)
# )
# openai.log = "debug"

## OPENAI
OPENAI_API_KEY = ''
OPENAI_BASE_URL = 'http://outproxy:9000/v1'
OPENAI_REQUEST_URL = OPENAI_BASE_URL + '/models'
OPENAI_STRUCT = OpenAI( api_key = '', base_url = OPENAI_BASE_URL )

ANTHRO_API_KEY = ''
ANTHRO_BASE_URL = 'https://api.openai.com/'

def set_openai_api_key( api_key ):
    OPENAI_API_KEY = api_key
    OPENAI_STRUCT.api_key = api_key

def set_anthro_api_key( api_key ):
    ANTHRO_API_KEY = api_key
    #OPENAI_STRUCT.api_key = api_key
    

# https://platform.openai.com/docs/models/model-endpoint-compatibility
ENDPOINT_DICT = {
    '/v1/chat/completions': ['gpt-4o', 'gpt-4o-mini'],
    '/v1/completions': [
        'text-davinci-003', 'text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001', 'davinci',
        'curie', 'babbage', 'ada'
    ],
    '/v1/edits': ['text-davinci-edit-001', 'code-davinci-edit-001'],
    '/v1/audio/transcriptions': ['whisper-1'],
    '/v1/audio/translations': ['whisper-1'],
    '/v1/fine-tunes': ['davinci', 'curie', 'babbage', 'ada'],
    '/v1/embeddings': ['text-embedding-ada-002', 'text-search-ada-doc-001'],
    '/vi/moderations': ['text-moderation-stable', 'text-moderation-latest']
}


def get_chat_model():
    return ENDPOINT_DICT['/v1/chat/completions']

def get_image_url_from_local(image):
    """
    Image is bytes, this function converts it to base64 and returns the image url
    """
    # Function to encode the image
    def encode_image(image):
        return base64.b64encode(image).decode('utf-8')

    base64_image = encode_image(image)
    return f'data:image/jpeg;base64,{base64_image}'

def get_message_obj(role, content):
    return {"role": role, "content": content}

def get_argument(model, system, messages, cur_text, temperature, top_p, frequency_penalty, presence_penalty, stream,
                     use_max_tokens, max_tokens,
                     is_json_response_available=0,
                     json_content=None
                 ):
    try:
        system_obj = get_message_obj("system", system)
        messages = [system_obj] + messages

        # Form argument
        openai_arg = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'top_p': top_p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'stream': stream,
        }
        if is_json_response_available:
            openai_arg['response_format'] = {"type": 'json_object'}
            cur_text += f' JSON {json_content}'

        openai_arg['messages'].append({"role": "user", "content": cur_text})

        if use_max_tokens:
            openai_arg['max_tokens'] = max_tokens

        return openai_arg
    except Exception as e:
        print(e)
        raise e

def form_response(response, info: ChatMessageContainer):
    info.content = response.choices[0].message.content
    info.prompt_tokens = response.usage.prompt_tokens
    info.completion_tokens = response.usage.completion_tokens
    info.total_tokens = response.usage.total_tokens
    info.finish_reason = response.choices[0].finish_reason
    return info
