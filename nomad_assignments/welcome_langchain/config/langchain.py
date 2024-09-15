import os
import json

KEY_FILE_NAME = 'api-key.json'


def setup_langchain_openai_envs(path: str = "./"):
    file_path = os.path.join(path, KEY_FILE_NAME)
    with open(file_path) as key_file:
        keys = json.load(key_file)

    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_API_KEY'] = keys['langchain-personal-key']
    os.environ['OPENAI_API_KEY'] = keys['openai_note-key']
