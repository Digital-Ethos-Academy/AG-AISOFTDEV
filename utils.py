# --- Helper Script for AI-Driven Software Engineering Course ---
# Description: This script provides a unified interface for interacting with
#              multiple LLM providers (OpenAI, Anthropic, Hugging Face, Google Gemini)
#              and simplifies common tasks like artifact management.
# -----------------------------------------------------------------

import os
import json
import requests
from PIL import Image
from io import BytesIO
import re
import base64
import time  # For loading indicator

# --- Dynamic Library Installation ---
try:
    from dotenv import load_dotenv
    from IPython.display import display, Markdown, Code, Image as IPyImage
    from plantuml import PlantUML
except ImportError:
    # Provide safe fallbacks so the module can be imported even when optional deps are missing.
    print("Warning: Optional core dependencies not found. Some features will be degraded.")
    print("To enable full functionality run: pip install python-dotenv ipython plantuml")

    # noop load_dotenv fallback
    def load_dotenv(*args, **kwargs):
        print("Warning: python-dotenv not installed; .env will not be loaded.")

    # minimal IPython.display fallbacks
    def display(*args, **kwargs):
        # no-op in non-notebook environments
        return None

    def Markdown(text):
        return text

    def Code(text):
        return text

    class IPyImage:
        def __init__(self, *args, **kwargs):
            # placeholder for notebook image object
            pass

    # PlantUML fallback
    class PlantUML:
        def __init__(self, url=None):
            print("Warning: plantuml not installed; rendering disabled.")
        def processes(self, *args, **kwargs):
            print("PlantUML rendering skipped (plantuml not installed).")


# --- Model & Provider Configuration ---

RECOMMENDED_MODELS = {
    # =========================
    # OpenAI — Text + Vision
    # =========================
    "gpt-5-nano-2025-08-07": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 400_000, "output_tokens": 128_000
    },
    "gpt-5-mini-2025-08-07": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 400_000, "output_tokens": 128_000
    },
    "gpt-5-2025-08-07": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 400_000, "output_tokens": 128_000
    },
    "gpt-4o": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 128_000, "output_tokens": 16_384
    },
    "gpt-4o-mini": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 128_000, "output_tokens": 16_384
    },
    "gpt-4.1": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_000_000, "output_tokens": 32_000
    },
    "gpt-4.1-mini": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_000_000, "output_tokens": 32_000
    },
    "gpt-4.1-nano": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_000_000, "output_tokens": 32_000
    },
    "gpt-4.5": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 128_000, "output_tokens": 16_384
    },
    "o3": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 200_000, "output_tokens": 100_000
    },
    "o4-mini": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 200_000, "output_tokens": 100_000
    },
    "codex-mini": {
        "provider": "openai", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 200_000, "output_tokens": 100_000
    },

    # =========================
    # OpenAI — Image / Audio
    # =========================
    "gpt-image-1": {
        "provider": "openai", "vision": True, "image_generation": True, "audio_transcription": False,
        "context_window_tokens": None, "output_tokens": None
    },
    "dall-e-3": {
        "provider": "openai", "vision": False, "image_generation": True, "audio_transcription": False,
        "context_window_tokens": None, "output_tokens": None
    },
    "whisper-1": {
        "provider": "openai", "vision": False, "image_generation": False, "audio_transcription": True,
        "context_window_tokens": None, "output_tokens": None
    },

    # =========================
    # Anthropic — Claude
    # =========================
    "claude-opus-4-1-20250805": {
        "provider": "anthropic", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 200_000, "output_tokens": 100_000
    },
    "claude-opus-4-20250514": {
        "provider": "anthropic", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 200_000, "output_tokens": 100_000
    },
    "claude-sonnet-4-20250514": {
        "provider": "anthropic", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_000_000, "output_tokens": 100_000
    },

    # ==========================================
    # Google — Gemini / Imagen / Speech-to-Text
    # ==========================================
    "gemini-2.5-pro": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_048_576, "output_tokens": 65_536
    },
    "gemini-2.5-flash": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_048_576, "output_tokens": 65_536
    },
    "gemini-2.5-flash-lite": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_048_576, "output_tokens": 65_536
    },
    "gemini-live-2.5-flash-preview": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_048_576, "output_tokens": 8_192
    },
    "gemini-2.5-flash-image-preview": {
        "provider": "google", "vision": True, "image_generation": True, "audio_transcription": False,
        "context_window_tokens": 32_768, "output_tokens": 32_768
    },
    "gemini-2.0-flash": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_048_576, "output_tokens": 8_192
    },
    "gemini-2.0-flash-lite": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_048_576, "output_tokens": 8_192
    },
    "gemini-2.0-flash-live-001": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_048_576, "output_tokens": 8_192
    },
    "gemini-deep-think": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_000_000, "output_tokens": 100_000
    },
    "gemini-veo-3": {
        "provider": "google", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": None, "output_tokens": None
    },
    "imagen-3.0-generate-002": {
        "provider": "google", "vision": False, "image_generation": True, "audio_transcription": False,
        "context_window_tokens": None, "output_tokens": None
    },
    "imagen-4.0-generate-001": {
        "provider": "google", "vision": False, "image_generation": True, "audio_transcription": False,
        "context_window_tokens": 480, "output_tokens": None
    },
    "google-cloud/speech-to-text/latest_long": {
        "provider": "google", "vision": False, "image_generation": False, "audio_transcription": True,
        "context_window_tokens": None, "output_tokens": None
    },
    "google-cloud/speech-to-text/latest_short": {
        "provider": "google", "vision": False, "image_generation": False, "audio_transcription": True,
        "context_window_tokens": None, "output_tokens": None
    },

    # =========================
    # Hugging Face — OSS
    # =========================
    "meta-llama/Llama-4-Scout-17B-16E-Instruct": {
        "provider": "huggingface", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 10_000_000, "output_tokens": 100_000
    },
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct": {
        "provider": "huggingface", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 1_000_000, "output_tokens": 100_000
    },
    "meta-llama/Llama-3.3-70B-Instruct": {
        "provider": "huggingface", "vision": False, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 4_096, "output_tokens": 1_024
    },
    "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.5": {
        "provider": "huggingface", "vision": False, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 4_096, "output_tokens": 1_024
    },
    "tokyotech-llm/Llama-3.1-Swallow-70B-Instruct-v0.3": {
        "provider": "huggingface", "vision": False, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 4_096, "output_tokens": 1_024
    },
    "mistralai/Mistral-7B-Instruct-v0.3": {
        "provider": "huggingface", "vision": False, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 32_768, "output_tokens": 8_192
    },
    "deepseek-ai/DeepSeek-V3": {
        "provider": "huggingface", "vision": False, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 128_000, "output_tokens": 100_000
    },
    "deepseek-ai/DeepSeek-V3-Small": {
        "provider": "huggingface", "vision": False, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 128_000, "output_tokens": 100_000
    },
    "deepseek-ai/DeepSeek-VL2": {
        "provider": "huggingface", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 32_000, "output_tokens": 8_000
    },
    "deepseek-ai/DeepSeek-VL2-Small": {
        "provider": "huggingface", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 32_000, "output_tokens": 8_000
    },
    "deepseek-ai/DeepSeek-VL2-Tiny": {
        "provider": "huggingface", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 32_000, "output_tokens": 8_000
    },
    "deepseek-ai/Janus-Pro-7B": {
        "provider": "huggingface", "vision": True, "image_generation": False, "audio_transcription": False,
        "context_window_tokens": 8_192, "output_tokens": 2_048
    },
}

def recommended_models_table(task=None, provider=None, vision=None, image_generation=None,
                             audio_transcription=None, min_context=None, min_output_tokens=None):
    """
    Return a markdown table of recommended models, optionally filtered by attributes.

    Args:
        task (str, optional): High level task to filter models. Accepts values like
            'vision', 'image', 'audio', or 'text'. These set sensible defaults for
            the corresponding capability flags unless explicitly provided.
        provider (str, optional): Filter models by provider name (e.g. ``'openai'``).
        vision (bool, optional): If set, include only models that match vision capability.
        image_generation (bool, optional): If set, include only image generation models.
        audio_transcription (bool, optional): If set, include only models supporting
            audio transcription.
        min_context (int, optional): Minimum context window size required.
        min_output_tokens (int, optional): Minimum max output tokens required.

    Returns:
        str: Markdown formatted table.
    """
    # Interpret task shortcuts
    if task:
        t = task.lower()
        if t in {"vision", "multimodal", "vl"} and vision is None:
            vision = True
        elif t in {"image", "image_generation", "image-generation"} and image_generation is None:
            image_generation = True
        elif t in {"audio", "speech", "audio_transcription", "stt"} and audio_transcription is None:
            audio_transcription = True
        elif t == "text":
            vision = False if vision is None else vision
            image_generation = False if image_generation is None else image_generation
            audio_transcription = False if audio_transcription is None else audio_transcription

    rows = []
    for model_name in sorted(RECOMMENDED_MODELS.keys()):
        cfg = RECOMMENDED_MODELS[model_name]
        model_provider = (cfg.get("provider") or "").lower()
        model_vision = cfg.get("vision", False)
        model_image = cfg.get("image_generation", False)
        model_audio = cfg.get("audio_transcription", False)

        # Prefer canonical integer fields used in RECOMMENDED_MODELS
        context = cfg.get("context_window_tokens")
        if context is None:
            # Backwards-compat: allow older key name
            context = cfg.get("context_window")

        max_tokens = cfg.get("output_tokens")
        if max_tokens is None:
            max_tokens = cfg.get("max_output_tokens")

        # Normalize provider filter to be case-insensitive
        if provider and model_provider != provider.lower():
            continue
        if vision is not None and bool(model_vision) != bool(vision):
            continue
        if image_generation is not None and bool(model_image) != bool(image_generation):
            continue
        if audio_transcription is not None and bool(model_audio) != bool(audio_transcription):
            continue
        if min_context and (context is None or (isinstance(context, int) and context < min_context)):
            continue
        if min_output_tokens and (max_tokens is None or (isinstance(max_tokens, int) and max_tokens < min_output_tokens)):
            continue

        def _fmt_num(x):
            if x is None:
                return "-"
            try:
                # format large ints with commas
                return f"{int(x):,}"
            except Exception:
                return str(x)

        rows.append(
            f"| {model_name} | {model_provider or '-'} | {'✅' if model_vision else '❌'} | "
            f"{'✅' if model_image else '❌'} | {'✅' if model_audio else '❌'} | "
            f"{_fmt_num(context)} | {_fmt_num(max_tokens)} |"
        )

    if not rows:
        return "No models match the specified criteria."

    header = (
        "| Model | Provider | Vision | Image Gen | Audio Transcription | Context Window | Max Output Tokens |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    table = header + "\n".join(rows)
    display(Markdown(table))
    return table

# --- Environment and API Client Setup ---

def load_environment():
    """Loads environment variables from a .env file in the project root."""
    path = os.getcwd()
    while path != os.path.dirname(path):
        if os.path.exists(os.path.join(path, '.env')) or os.path.exists(os.path.join(path, '.git')):
            project_root = path
            break
        path = os.path.dirname(path)
    else:
        project_root = os.getcwd()

    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print("Warning: .env file not found. API keys may not be loaded.")


def setup_llm_client(model_name="gpt-4o"):
    """
    Configures and returns an LLM client based on the specified model name.
    Supports OpenAI, Anthropic, Hugging Face, and Google Gemini.
    """
    load_environment()
    if model_name not in RECOMMENDED_MODELS:
        print(f"ERROR: Model '{model_name}' is not in the list of recommended models.")
        return None, None, None
    config = RECOMMENDED_MODELS[model_name]
    api_provider = config["provider"]
    client = None
    try:
        if api_provider == "openai":
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in .env file.")
            client = OpenAI(api_key=api_key)
        elif api_provider == "anthropic":
            from anthropic import Anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in .env file.")
            client = Anthropic(api_key=api_key)
        elif api_provider == "huggingface":
            from huggingface_hub import InferenceClient
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not api_key:
                raise ValueError("HUGGINGFACE_API_KEY not found in .env file.")
            client = InferenceClient(model=model_name, token=api_key)
        elif api_provider == "gemini" or api_provider == "google": # Google for image generation or STT
            if config.get("audio_transcription"):
                from google.cloud import speech
                client = speech.SpeechClient()
            else:
                import google.generativeai as genai
                api_key = os.getenv("GOOGLE_API_KEY")  # Use GOOGLE_API_KEY for both Gemini text and Imagen
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY not found in .env file.")
                genai.configure(api_key=api_key)
                if config["image_generation"]:
                    # For image generation, the client is not directly a GenerativeModel instance
                    # but rather the genai module itself for the predict call.
                    client = genai
                else:
                    client = genai.GenerativeModel(model_name)
    except ImportError:
        print(f"ERROR: The required library for '{api_provider}' is not installed.")
        return None, None, None
    except ValueError as e:
        print(f"ERROR: {e}")
        return None, None, None
    print(f"✅ LLM Client configured: Using '{api_provider}' with model '{model_name}'")
    return client, model_name, api_provider

# --- Core Interaction Functions ---

def get_completion(prompt, client, model_name, api_provider, temperature=0.7):
    """Sends a text-only prompt to the LLM and returns the completion."""
    if not client:
        return "API client not initialized."
    try:
        if api_provider == "openai":
            response = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}], temperature=temperature)
            return response.choices[0].message.content
        elif api_provider == "anthropic":
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        elif api_provider == "huggingface":
            response = client.chat_completion(messages=[{"role": "user", "content": prompt}], temperature=max(0.1, temperature), max_tokens=4096)
            return response.choices[0].message.content
        elif api_provider == "gemini":
            response = client.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"An API error occurred: {e}"

def get_vision_completion(prompt, image_url, client, model_name, api_provider):
    """Sends an image and a text prompt to a vision-capable LLM and returns the completion."""
    if not client:
        return "API client not initialized."
    if not RECOMMENDED_MODELS.get(model_name, {}).get("vision"):
        return f"Error: Model '{model_name}' does not support vision."
    try:
        # Fetch image from URL and convert to base64 for Gemini/HuggingFace if needed, or pass URL for OpenAI
        if api_provider == "openai":
            response = client.chat.completions.create(model=model_name, messages=[{"role": "user", 
                                                                                   "content": [{"type": "text", 
                                                                                                "text": prompt}, 
                                                                                               {"type": "image_url", 
                                                                                                "image_url": {"url": image_url}}]}], 
                                                                                                max_tokens=4096)
            return response.choices[0].message.content
        elif api_provider == "anthropic":
            response_img = requests.get(image_url)
            response_img.raise_for_status()
            img_data = base64.b64encode(response_img.content).decode('utf-8')
            mime_type = response_img.headers['Content-Type']
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image", "source": {"type": "base64", "media_type": mime_type, "data": img_data}}
                    ]
                }]
            )
            return response.content[0].text
        elif api_provider == "gemini":
            # For Gemini, we need to convert the image URL to inlineData (base64)
            response_img = requests.get(image_url)
            response_img.raise_for_status()
            img_data = base64.b64encode(response_img.content).decode('utf-8')
            mime_type = response_img.headers['Content-Type']

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt},
                            {"inlineData": {"mimeType": mime_type, "data": img_data}}
                        ]
                    }
                ]
            }
            # Use the raw genai client for direct API call
            # The client here is actually `genai` module from setup_llm_client
            api_key = "" # Canvas will provide this.
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"Unexpected Gemini vision response structure: {result}"
        elif api_provider == "huggingface":
            response_img = requests.get(image_url)
            response_img.raise_for_status()
            img = Image.open(BytesIO(response_img.content))
            response = client.image_to_text(image=img, prompt=prompt)
            return response
    except Exception as e:
        return f"An API error occurred during vision completion: {e}"

def get_image_generation_completion(prompt, client, model_name, api_provider):
    """Generates an image from a text prompt using an image generation LLM."""
    if not client:
        return "API client not initialized."
    if not RECOMMENDED_MODELS.get(model_name, {}).get("image_generation"):
        return f"Error: Model '{model_name}' does not support image generation."

    # Display a loading indicator
    print("Generating image... This may take a moment.")
    display(Markdown("⏳ Generating image..."))
    start_time = time.time()

    try:
        if api_provider == "openai":
            response = client.images.generate(model=model_name, prompt=prompt)
            image_b64 = response.data[0].b64_json
        elif api_provider == "google":
            if model_name.startswith("imagen"):
                payload = {"instances": {"prompt": prompt}, "parameters": {"sampleCount": 1}}
                apiKey = ""  # Canvas will automatically provide this.
                apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:predict?key={apiKey}"
                response = requests.post(apiUrl, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
                response.raise_for_status()
                result = response.json()
                if result.get("predictions") and len(result["predictions"]) > 0 and result["predictions"][0].get("bytesBase64Encoded"):
                    image_b64 = result["predictions"][0]["bytesBase64Encoded"]
                else:
                    return f"Error: Unexpected image generation response structure: {result}"
            else:
                model = client.GenerativeModel(model_name)
                result = model.generate_images(prompt=prompt)
                image_b64 = result.images[0].base64_data
        else:
            return f"Error: Image generation not implemented for provider '{api_provider}'"

        image_url = f"data:image/png;base64,{image_b64}"
        end_time = time.time()
        print(f"✅ Image generated in {end_time - start_time:.2f} seconds.")
        return image_url
    except Exception as e:
        return f"An API error occurred during image generation: {e}"


def transcribe_audio(audio_path, client, model_name, api_provider, language_code="en-US"):
    """Transcribes audio from a file using a speech-to-text model."""
    if not client:
        return "API client not initialized."
    if not RECOMMENDED_MODELS.get(model_name, {}).get("audio_transcription"):
        return f"Error: Model '{model_name}' does not support audio transcription."

    try:
        if api_provider == "openai":
            with open(audio_path, "rb") as f:
                response = client.audio.transcriptions.create(model=model_name, file=f)
            return getattr(response, "text", response.get("text"))
        elif api_provider == "google":
            from google.cloud import speech
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(language_code=language_code)
            response = client.recognize(config=config, audio=audio)
            if response.results and response.results[0].alternatives:
                return response.results[0].alternatives[0].transcript
            return "No transcription available."
        else:
            return f"Error: Audio transcription not implemented for provider '{api_provider}'"
    except Exception as e:
        return f"An API error occurred during audio transcription: {e}"


def clean_llm_output(output_str: str, language: str = 'json') -> str:
    """
    Cleans markdown code fences from LLM output.
    Supports various languages.
    """
    if '```' in output_str:
        # Regex to find code blocks with optional language specifier
        # It looks for ```[language_optional]\n[content]\n```
        pattern = re.compile(r'```(?:' + re.escape(language) + r')?\s*\n(.*?)\n```', re.DOTALL | re.IGNORECASE)
        match = pattern.search(output_str)
        if match:
            return match.group(1).strip()
        else:
            # Fallback if regex doesn't match perfectly (e.g., no language specified, or extra text)
            parts = output_str.split('```')
            if len(parts) >= 3:
                # Take the content between the first and second ```
                return parts[1].strip()
            else:
                # If only one ``` or malformed, return original string
                return output_str.strip()
    return output_str.strip()


# --- Artifact Management & Display ---

def _find_project_root():
    """
    Finds the project root by searching upwards for a known directory marker
    (like '.git' or 'artifacts'). This is more reliable than just using os.getcwd().
    """
    path = os.getcwd()
    while path != os.path.dirname(path):  # Stop at the filesystem root
        # Check for multiple common markers to increase reliability
        if any(os.path.exists(os.path.join(path, marker)) for marker in ['.git', 'artifacts', 'README.md']):
            return path
        path = os.path.dirname(path)
    # Fallback if no markers are found (e.g., in a bare directory)
    print("Warning: Project root marker not found. Defaulting to current directory.")
    return os.getcwd()


def save_artifact(content, file_path):
    """Saves content to a specified file path, creating directories if needed."""
    try:
        project_root = _find_project_root()
        full_path = os.path.join(project_root, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully saved artifact to: {file_path}")
    except Exception as e:
        print(f"❌ Error saving artifact to {file_path}: {e}")

def load_artifact(file_path):
    """Loads content from a specified file path."""
    try:
        project_root = _find_project_root()
        full_path = os.path.join(project_root, file_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: Artifact file not found at {file_path}.")
        return None

def render_plantuml_diagram(puml_code, output_path="artifacts/diagram.png"):
    """Renders PlantUML code and saves it as a PNG image."""
    try:
        # FIX: Corrected the PlantUML URL
        pl = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        project_root = _find_project_root()
        
        full_path = os.path.join(project_root, output_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        pl.processes(puml_code, outfile=full_path)
        print(f"✅ Diagram rendered and saved to: {output_path}")
        display(IPyImage(url=full_path))
    except Exception as e:
        print(f"❌ Error rendering PlantUML diagram: {e}")

