"""
This file is used to store the constants and the global variables that are used throughout the application.
"""

import json
import os
import shutil
import sys

import tomllib  # Python 3.11 built-in module
from pathlib import Path

# Load the pyproject.toml file
SRC_DIR = Path(__file__).resolve().parent # VividNode/pyqt_openai
ROOT_DIR = SRC_DIR.parent # VividNode
SETUP_FILENAME = ROOT_DIR / "pyproject.toml"

# Read the TOML file using tomllib (Python 3.11+)
with open(SETUP_FILENAME, "rb") as file:
    pyproject_data = tomllib.load(file)

# For the sake of following the PEP8 standard, we will declare module-level dunder names.
# PEP8 standard about dunder names: https://peps.python.org/pep-0008/#module-level-dunder-names

__version__ = pyproject_data["project"]["version"]
__author__ = pyproject_data["project"]["authors"][0]['name']

# Constants
# ----------------------------
# APP
PACKAGE_NAME = pyproject_data["project"]["name"]
OWNER = 'yjg30737'

DEFAULT_APP_NAME = 'VividNode'

# Check if the application is frozen (compiled with PyInstaller)
# If this is main.py, it will return False, that means it is not frozen.
def is_frozen():
    return hasattr(sys, 'frozen')

# The executable path of the application
def get_executable_path():
    if is_frozen():  # For PyInstaller
        executable_path = sys._MEIPASS
    else:
        executable_path = os.path.dirname(os.path.abspath(__file__))
    return executable_path

EXEC_PATH = get_executable_path()

# The current filename of the application
CURRENT_FILENAME = os.path.join(EXEC_PATH, f'{DEFAULT_APP_NAME}.exe')

def get_config_directory():
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.getenv('APPDATA'), DEFAULT_APP_NAME)
    elif os.name == 'posix':  # macOS/Linux
        config_dir = os.path.join(os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config')), DEFAULT_APP_NAME)
    else:
        config_dir = os.path.expanduser(f'~/.{DEFAULT_APP_NAME}')  # Fallback

    # Ensure the directory exists
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    return config_dir


CONTACT = pyproject_data["project"]["authors"][0]['email']
APP_INITIAL_WINDOW_SIZE = (1280, 768)

TRANSPARENT_RANGE = 20, 100
TRANSPARENT_INIT_VAL = 100

LICENSE = pyproject_data["project"]["license"]['text']
LICENSE_URL = 'https://github.com/yjg30737/pyqt-openai/blob/main/LICENSE'
KOFI_URL = 'https://ko-fi.com/junggyuyoon'
PAYPAL_URL = 'https://paypal.me/yjg30737'
GITHUB_URL = 'https://github.com/yjg30737/pyqt-openai'
DISCORD_URL = 'https://discord.gg/cHekprskVE'

QUICKSTART_MANUAL_URL = 'https://medium.com/@yjg30737/what-is-vividnode-how-to-use-it-4d8a9269a3c0'
LLAMAINDEX_URL = 'https://medium.com/@yjg30737/what-is-llamaindex-9b821d66568f'
HOW_TO_GET_OPENAI_API_KEY_URL = 'https://medium.com/@yjg30737/how-to-get-your-openai-api-key-e2193850932e'
HOW_TO_EXPORT_CHATGPT_CONVERSATION_HISTORY_URL = 'https://medium.com/@yjg30737/how-to-export-your-chatgpt-conversation-history-caa0946d6349'
HOW_TO_REPLICATE = 'https://medium.com/@yjg30737/10a2cb983ceb'

COLUMN_TO_EXCLUDE_FROM_SHOW_HIDE_CHAT = ['id']
COLUMN_TO_EXCLUDE_FROM_SHOW_HIDE_IMAGE = ['id', 'data']

MESSAGE_PADDING = 16
MESSAGE_MAXIMUM_HEIGHT = 800
MAXIMUM_MESSAGES_IN_PARAMETER = 20
MESSAGE_MAXIMUM_HEIGHT_RANGE = 300, 1000
MAXIMUM_MESSAGES_IN_PARAMETER_RANGE = 2, 1000

CONTEXT_DELIMITER = '\n'*2
PROMPT_IMAGE_SCALE = 200, 200
TOAST_DURATION = 3

## PARAMETER - OPENAI CHAT
OPENAI_TEMPERATURE_RANGE = 0, 2
OPENAI_TEMPERATURE_STEP = 0.01

MAX_TOKENS_RANGE = 512, 128000

TOP_P_RANGE = 0, 1
TOP_P_STEP = 0.01

FREQUENCY_PENALTY_RANGE = 0, 2
FREQUENCY_PENALTY_STEP = 0.01

PRESENCE_PENALTY_RANGE = 0, 2
PRESENCE_PENALTY_STEP = 0.01

ICON_PATH = os.path.join(EXEC_PATH, 'ico')

## ICONS
DEFAULT_APP_ICON = os.path.join(ICON_PATH, 'icon.ico')

ICON_ADD = os.path.join(ICON_PATH, 'add.svg')
ICON_CASE = os.path.join(ICON_PATH, 'case.svg')
ICON_CLOSE = os.path.join(ICON_PATH, 'close.svg')
ICON_COPY = os.path.join(ICON_PATH, 'copy.svg')
ICON_CUSTOMIZE = os.path.join(ICON_PATH, 'customize.svg')
ICON_DELETE = os.path.join(ICON_PATH, 'delete.svg')
ICON_DISCORD = os.path.join(ICON_PATH, 'discord.svg')
ICON_EXPORT = os.path.join(ICON_PATH, 'export.svg')
ICON_FAVORITE_NO = os.path.join(ICON_PATH, 'favorite_no.svg')
ICON_FAVORITE_YES = os.path.join(ICON_PATH, 'favorite_yes.svg')
ICON_FOCUS_MODE = os.path.join(ICON_PATH, 'focus_mode.svg')
ICON_FULLSCREEN = os.path.join(ICON_PATH, 'fullscreen.svg')
ICON_GITHUB = os.path.join(ICON_PATH, 'github.svg')
ICON_HELP = os.path.join(ICON_PATH, 'help.svg')
ICON_HISTORY = os.path.join(ICON_PATH, 'history.svg')
ICON_IMPORT = os.path.join(ICON_PATH, 'import.svg')
ICON_INFO = os.path.join(ICON_PATH, 'info.svg')
ICON_NEXT = os.path.join(ICON_PATH, 'next.svg')
ICON_OPENAI = os.path.join(ICON_PATH, 'openai.png')
ICON_PREV = os.path.join(ICON_PATH, 'prev.svg')
ICON_PROMPT = os.path.join(ICON_PATH, 'prompt.svg')
ICON_QUESTION = os.path.join(ICON_PATH, 'question.svg')
ICON_REFRESH = os.path.join(ICON_PATH, 'refresh.svg')
ICON_REGEX = os.path.join(ICON_PATH, 'regex.svg')
ICON_SAVE = os.path.join(ICON_PATH, 'save.svg')
ICON_SEARCH = os.path.join(ICON_PATH, 'search.svg')
ICON_SETTING = os.path.join(ICON_PATH, 'setting.svg')
ICON_SIDEBAR = os.path.join(ICON_PATH, 'sidebar.svg')
ICON_STACKONTOP = os.path.join(ICON_PATH, 'stackontop.svg')
ICON_USER = os.path.join(ICON_PATH, 'user.png')
ICON_VERTICAL_THREE_DOTS = os.path.join(ICON_PATH, 'vertical_three_dots.svg')
ICON_WORD = os.path.join(ICON_PATH, 'word.svg')
ICON_SEND = os.path.join(ICON_PATH, 'send.svg')

## CUSTOMIZE
DEFAULT_ICON_SIZE = (24, 24)
DEFAULT_USER_IMAGE_PATH = ICON_USER
DEFAULT_AI_IMAGE_PATH = ICON_OPENAI
DEFAULT_FONT_SIZE = 14
DEFAULT_FONT_FAMILY = 'Arial'

DEFAULT_BUTTON_HOVER_COLOR = '#A2D0DD'
DEFAULT_BUTTON_PRESSED_COLOR = '#B3E0FF'
DEFAULT_BUTTON_CHECKED_COLOR = '#B3E0FF'
DEFAULT_SOURCE_HIGHLIGHT_COLOR = '#CCB500'
DEFAULT_SOURCE_ERROR_COLOR = '#FF0000'
DEFAULT_FOUND_TEXT_COLOR = '#00A2E8'
DEFAULT_FOUND_TEXT_BG_COLOR = '#FFF200'

DEFAULT_LINK_COLOR = '#4F93FF'
DEFAULT_LINK_HOVER_COLOR = '#FF0000'

DEFAULT_TOAST_BACKGROUND_COLOR = '#444444'
DEFAULT_TOAST_FOREGROUND_COLOR = '#EEEEEE'

## MARKDOWN
# I am not planning to use it at the moment.
# DEFAULT_MARKDOWN_span_font = 'Courier New'
# DEFAULT_MARKDOWN_span_color = '#000'
# DEFAULT_MARKDOWN_ul_color = '#000'
# DEFAULT_MARKDOWN_h1_color = '#000'
# DEFAULT_MARKDOWN_h2_color = '#000'
# DEFAULT_MARKDOWN_h3_color = '#000'
# DEFAULT_MARKDOWN_h4_color = '#000'
# DEFAULT_MARKDOWN_h5_color = '#000'
# DEFAULT_MARKDOWN_h6_color = '#000'
# DEFAULT_MARKDOWN_a_color = '#000'

## SHORTCUT
DEFAULT_SHORTCUT_GENERAL_ACTION = 'Return'
DEFAULT_SHORTCUT_FIND_PREV = 'Ctrl+Shift+D'
DEFAULT_SHORTCUT_FIND_NEXT = 'Ctrl+D'
DEFAULT_SHORTCUT_FIND_CLOSE = 'Escape'
DEFAULT_SHORTCUT_PROMPT_BEGINNING = 'Ctrl+B'
DEFAULT_SHORTCUT_PROMPT_ENDING = 'Ctrl+E'
DEFAULT_SHORTCUT_SUPPORT_PROMPT_COMMAND = 'Ctrl+Shift+P'
DEFAULT_SHORTCUT_STACK_ON_TOP = 'Ctrl+Shift+S'
DEFAULT_SHORTCUT_SHOW_TOOLBAR = 'Ctrl+T'
DEFAULT_SHORTCUT_SHOW_SECONDARY_TOOLBAR = 'Ctrl+Shift+T'
DEFAULT_SHORTCUT_FOCUS_MODE = 'F10'
DEFAULT_SHORTCUT_FULL_SCREEN = 'F11'
DEFAULT_SHORTCUT_FIND = 'Ctrl+F'
DEFAULT_SHORTCUT_JSON_MODE = 'Ctrl+J'
DEFAULT_SHORTCUT_LEFT_SIDEBAR_WINDOW = 'Ctrl+L'
DEFAULT_SHORTCUT_RIGHT_SIDEBAR_WINDOW = 'Ctrl+R'
DEFAULT_SHORTCUT_CONTROL_PROMPT_WINDOW = 'Ctrl+Shift+C'
DEFAULT_SHORTCUT_SETTING = 'Ctrl+Alt+S'
DEFAULT_SHORTCUT_SEND = 'Ctrl+Return'

## DIRECTORY PATH & FILE'S NAME
MAIN_INDEX = 'main.py'
IMAGE_DEFAULT_SAVE_DIRECTORY = 'image_result'
INI_FILE_NAME = os.path.join(get_config_directory(), 'config.yaml')

DB_FILE_NAME = 'conv'
FILE_NAME_LENGTH = 32
QFILEDIALOG_DEFAULT_DIRECTORY = os.path.expanduser('~')

## EXTENSIONS
TEXT_FILE_EXT_LIST = ['.txt']
IMAGE_FILE_EXT_LIST = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
IMAGE_FILE_EXT_LIST_STR = 'Image File (*.png *.jpg *.jpeg *.gif *.bmp)'
TEXT_FILE_EXT_LIST_STR = 'Text File (*.txt)'
JSON_FILE_EXT_LIST_STR = 'JSON File (*.json)'
READ_FILE_EXT_LIST_STR = f'{TEXT_FILE_EXT_LIST_STR};;{IMAGE_FILE_EXT_LIST_STR}'

## PROMPT
PROMPT_BEGINNING_KEY_NAME = 'prompt_beginning'
PROMPT_JSON_KEY_NAME = 'prompt_json'
PROMPT_MAIN_KEY_NAME = 'prompt_main'
PROMPT_END_KEY_NAME = 'prompt_ending'
PROMPT_NAME_REGEX = '^[a-zA-Z_0-9]+$'
INDENT_SIZE = 4
NOTIFIER_MAX_CHAR = 100

# DB
DB_NAME_REGEX = '[a-zA-Z0-9]{1,20}'

THREAD_TABLE_NAME_OLD = 'conv_tb'
THREAD_TRIGGER_NAME_OLD = 'conv_tr'
MESSAGE_TABLE_NAME_OLD = 'conv_unit_tb'

THREAD_TABLE_NAME = 'thread_tb'
THREAD_TRIGGER_NAME = 'thread_tr'
MESSAGE_TABLE_NAME = 'message_tb'

IMAGE_TABLE_NAME = 'image_tb'

THREAD_MESSAGE_INSERTED_TR_NAME_OLD = 'conv_tb_updated_by_unit_inserted_tr'
THREAD_MESSAGE_UPDATED_TR_NAME_OLD = 'conv_tb_updated_by_unit_updated_tr'
THREAD_MESSAGE_DELETED_TR_NAME_OLD = 'conv_tb_updated_by_unit_deleted_tr'

THREAD_MESSAGE_INSERTED_TR_NAME = 'thread_message_inserted_tr'
THREAD_MESSAGE_UPDATED_TR_NAME = 'thread_message_updated_tr'
THREAD_MESSAGE_DELETED_TR_NAME = 'thread_message_deleted_tr'

THREAD_ORDERBY = 'update_dt'

PROPERTY_PROMPT_GROUP_TABLE_NAME_OLD = 'prop_prompt_grp_tb'
PROPERTY_PROMPT_UNIT_TABLE_NAME_OLD = 'prop_prompt_unit_tb'
TEMPLATE_PROMPT_GROUP_TABLE_NAME_OLD = 'template_prompt_grp_tb'
TEMPLATE_PROMPT_TABLE_NAME_OLD = 'template_prompt_tb'
PROPERTY_PROMPT_UNIT_DEFAULT_VALUE = [{'name': 'Task', 'content': ''},
                                      {'name': 'Topic', 'content': ''},
                                      {'name': 'Style', 'content': ''},
                                      {'name': 'Tone', 'content': ''},
                                      {'name': 'Audience', 'content': ''},
                                      {'name': 'Length', 'content': ''},
                                      {'name': 'Form', 'content': ''}]

PROMPT_GROUP_TABLE_NAME = 'prompt_group_tb'
PROMPT_ENTRY_TABLE_NAME = 'prompt_entry_tb'

# DEFAULT JSON FILENAME FOR PROMPT
AWESOME_CHATGPT_PROMPTS_FILENAME = 'prompt_res/awesome_chatgpt_prompts.json'
ALEX_BROGAN_PROMPT_FILENAME = 'prompt_res/alex_brogan.json'

FORM_PROMPT_GROUP_SAMPLE = json.dumps([
    {
        "name": 'Default',
        "data": PROPERTY_PROMPT_UNIT_DEFAULT_VALUE
    }
], indent=INDENT_SIZE)

SENTENCE_PROMPT_GROUP_SAMPLE = '''[
    {
        "name": "alex_brogan",
        "data": [
            {
                "name": "sample_1",
                "content": "Identify the 20% of [topic or skill] that will yield 80% of the desired results and provide a focused learning plan to master it."
            },
            {
                "name": "sample_2",
                "content": "Explain [topic or skill] in the simplest terms possible as if teaching it to a complete beginner. Identify gaps in my understanding and suggest resources to fill them."
            }
        ]
    },
    {
        "name": "awesome_chatGPT_prompts",
        "data": [
            {
                "name": "linux_terminal",
                "content": "I want you to act as a linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. do not write explanations. do not type commands unless I instruct you to do so. when i need to tell you something in english, i will do so by putting text inside curly brackets {like this}. my first command is pwd"
            },
            {
                "name": "english_translator_and_improver",
                "content": "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. My first sentence is \"istanbulu cok seviyom burada olmak cok guzel\""
            },
        ]
    }
]'''

# Load the default prompt
if os.path.exists(AWESOME_CHATGPT_PROMPTS_FILENAME):
    AWESOME_CHATGPT_PROMPTS = json.load(open(AWESOME_CHATGPT_PROMPTS_FILENAME))[0]
if os.path.exists(ALEX_BROGAN_PROMPT_FILENAME):
    ALEX_BROGAN_PROMPT = json.load(open(ALEX_BROGAN_PROMPT_FILENAME))[0]

# DEFAULT Configuration data for the application settings
# Initialize here to avoid circular import
# ----------------------------
CONFIG_DATA = {
    'General': {
        'TAB_IDX': 0,
        'show_chat_list': True,
        'stream': True,
        'db': 'conv',
        'model': 'gpt-4o',
        'show_setting': True,
        'use_llama_index': False,
        'do_not_ask_again': False,
        'show_prompt': True,
        'system': 'You are a helpful assistant.',
        'notify_finish': True,
        'temperature': 1,
        'max_tokens': -1,
        'show_toolbar': True,
        'show_secondary_toolbar': True,
        'top_p': 1,
        'chat_column_to_show': ['id', 'name', 'insert_dt', 'update_dt'],
        'frequency_penalty': 0,
        'image_column_to_show': ['id', 'model', 'width', 'height', 'prompt', 'negative_prompt', 'n', 'quality', 'data', 'style', 'revised_prompt', 'update_dt', 'insert_dt'],
        'presence_penalty': 0,
        'json_object': False,
        'maximum_messages_in_parameter': MAXIMUM_MESSAGES_IN_PARAMETER,
        'show_as_markdown': True,
        'run_at_startup': True,
        'use_max_tokens': False,
        'background_image': '',
        'user_image': DEFAULT_USER_IMAGE_PATH,
        'ai_image': DEFAULT_AI_IMAGE_PATH,
        'font_size': DEFAULT_FONT_SIZE,
        'font_family': DEFAULT_FONT_FAMILY,
        'API_KEY': '',
        'llama_index_directory': '',
        'apply_user_defined_styles': False,
        'focus_mode': False,
    },
    'DALLE': {
        'quality': 'standard',
        'show_history': True,
        'n': 1,
        'show_setting': True,
        'size': '1024x1024',
        'directory': QFILEDIALOG_DEFAULT_DIRECTORY,
        'is_save': True,
        'continue_generation': False,
        'number_of_images_to_create': 2,
        'style': 'vivid',
        'response_format': 'b64_json',
        'save_prompt_as_text': True,
        'show_prompt_on_image': False,
        'prompt_type': 1,
        'width': 1024,
        'height': 1024,
        'prompt': "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
    },
    'REPLICATE': {
        'REPLICATE_API_TOKEN': '',
        'show_history': True,
        'model': 'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
        'show_setting': True,
        'width': 768,
        'height': 768,
        'prompt': "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k",
        'negative_prompt': "ugly, deformed, noisy, blurry, distorted",
        'directory': QFILEDIALOG_DEFAULT_DIRECTORY,
        'is_save': True,
        'continue_generation': False,
        'number_of_images_to_create': 2,
        'save_prompt_as_text': True,
        'show_prompt_on_image': False
    }
}

# Update the __all__ list with the PEP8 standard dunder names
__all__ = ['__version__',
           '__author__']

# Update the __all__ list with the constants
__all__.extend([name for name, value in globals().items() if name.isupper()])
