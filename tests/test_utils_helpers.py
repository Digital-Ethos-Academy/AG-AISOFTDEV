import os
import uuid
from utils import clean_llm_output, save_artifact, load_artifact, _find_project_root


def test_clean_llm_output():
    raw = "```json\n{\"a\": 1}\n```"
    assert clean_llm_output(raw, language="json") == '{"a": 1}'


def test_save_and_load_artifact():
    filename = f"artifacts/{uuid.uuid4().hex}.txt"
    content = "hello"
    save_artifact(content, filename)
    try:
        assert load_artifact(filename) == content
    finally:
        full_path = os.path.join(_find_project_root(), filename)
        if os.path.exists(full_path):
            os.remove(full_path)
            dir_path = os.path.dirname(full_path)
            if os.path.isdir(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)
