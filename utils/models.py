"""Model metadata and helper utilities."""
from __future__ import annotations

from typing import Any, Dict

from .settings import display, Markdown

# --- Model & Provider Configuration ---
RECOMMENDED_MODELS: Dict[str, Dict[str, Any]] = {
    "gpt-5-nano-2025-08-07": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 400_000, "output_tokens": 128_000},
    "gpt-5-mini-2025-08-07": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 400_000, "output_tokens": 128_000},
    "gpt-5-2025-08-07": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 400_000, "output_tokens": 128_000},
    "gpt-4o": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 128_000, "output_tokens": 16_384},
    "gpt-4o-mini": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 128_000, "output_tokens": 16_384},
    "gpt-4.1": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_000_000, "output_tokens": 32_768},
    "gpt-4.1-mini": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_000_000, "output_tokens": 32_000},
    "gpt-4.1-nano": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_000_000, "output_tokens": 32_000},
    "o3": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 200_000, "output_tokens": 100_000},
    "o4-mini": {"provider": "openai", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 200_000, "output_tokens": 100_000},
    "dall-e-3": {"provider": "openai", "vision": False, "text_generation": False, "image_generation": True, "image_modification": False, "audio_transcription": False, "context_window_tokens": None, "output_tokens": None},
    #"gpt-image-1": {"provider": "openai", "vision": False, "text_generation": False, "image_generation": True, "image_modification": True, "audio_transcription": False, "context_window_tokens": None, "output_tokens": None},
    #"gpt-image-1-mini": {"provider": "openai", "vision": False, "text_generation": False, "image_generation": True, "image_modification": True, "audio_transcription": False, "context_window_tokens": None, "output_tokens": None},
    "gpt-4o-transcribe": {"provider": "openai", "vision": False, "text_generation": False, "image_generation": False, "image_modification": False, "audio_transcription": True, "context_window_tokens": None, "output_tokens": None},
    "gpt-4o-mini-transcribe":  {"provider": "openai", "vision": False, "text_generation": False, "image_generation": False, "image_modification": False, "audio_transcription": True, "context_window_tokens": None, "output_tokens": None},
    "whisper-1": {"provider": "openai", "vision": False, "text_generation": False, "image_generation": False, "image_modification": False, "audio_transcription": True, "context_window_tokens": None, "output_tokens": None},
    "claude-sonnet-4-5-20250929": {"provider": "anthropic", "vision": True, "text_generation": True, "context_window_tokens": 200_000, "output_tokens": 64_000},
    "claude-haiku-4-5-20251001":  {"provider": "anthropic", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 200_000, "output_tokens": 64_000},
    "claude-opus-4-1-20250805":   {"provider": "anthropic", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 200_000, "output_tokens": 32_000},
    "gemini-2.5-pro": {"provider": "google", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_048_576, "output_tokens": 65_536},
    "gemini-2.5-flash": {"provider": "google", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_048_576, "output_tokens": 65_536},
    "gemini-2.5-flash-lite": {"provider": "google", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_048_576, "output_tokens": 65_536},
    "gemini-live-2.5-flash-preview": {"provider": "google", "vision": False, "text_generation": False, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_048_576, "output_tokens": 8_192},
    "gemini-2.5-flash-image-preview": {"provider": "google", "vision": False, "text_generation": False, "image_generation": True, "image_modification": True, "audio_transcription": False, "context_window_tokens": 32_768, "output_tokens": 32_768},
    "gemini-2.0-flash-preview-image-generation": {"provider": "google", "vision": False, "text_generation": False, "image_generation": True, "image_modification": True, "audio_transcription": False, "context_window_tokens": 32_000, "output_tokens": 8_192},
    "gemini-1.5-pro": {"provider": "google", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 2_000_000, "output_tokens": 8_192},
    "gemini-1.5-flash": {"provider": "google", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_000_000, "output_tokens": 8_192},
    "gemini-2.0-flash-exp": {"provider": "google", "vision": True, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_048_576, "output_tokens": 8_192},
    "veo-3.1-generate-preview": {"provider": "google", "vision": False, "text_generation": False, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_024, "output_tokens": None},
    "veo-3.1-fast-generate-preview": {"provider": "google", "vision": False, "text_generation": False, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_024, "output_tokens": None},
    "meta-llama/Llama-4-Scout-17B-16E-Instruct": {"provider": "huggingface", "vision": False, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 10_000_000, "output_tokens": 100_000},
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct": {"provider": "huggingface", "vision": False, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 1_000_000, "output_tokens": 100_000},
    "meta-llama/Llama-3.3-70B-Instruct": {"provider": "huggingface", "vision": False, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 8_192, "output_tokens": 4_096},
    "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.5": {"provider": "huggingface", "vision": False, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 4_096, "output_tokens": 1_024},
    "mistralai/Mistral-7B-Instruct-v0.3": {"provider": "huggingface", "vision": False, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 32_768, "output_tokens": 8_192},
    "deepseek-ai/DeepSeek-V3.1": {"provider": "huggingface", "vision": False, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 128_000, "output_tokens": 100_000},
    "Qwen/Qwen-Image": {"provider": "huggingface", "vision": False, "text_generation": False, "image_generation": True, "image_modification": False, "audio_transcription": False, "context_window_tokens": None, "output_tokens": None},
    "Qwen/Qwen-Image-Edit": {"provider": "huggingface", "vision": False, "text_generation": False, "image_generation": False, "image_modification": True, "audio_transcription": False, "context_window_tokens": None, "output_tokens": None},
    "stabilityai/stable-diffusion-3.5-large": {"provider": "huggingface", "vision": False, "text_generation": False, "image_generation": True, "image_modification": False, "audio_transcription": False, "context_window_tokens": None, "output_tokens": None},
    "black-forest-labs/FLUX.1-Kontext-dev": {"provider": "huggingface", "vision": False, "text_generation": False, "image_generation": False, "image_modification": True, "audio_transcription": False, "context_window_tokens": None, "output_tokens": None},
    "MiniMaxAI/MiniMax-M2": {"provider": "huggingface", "vision": False, "text_generation": True, "image_generation": False, "image_modification": False, "audio_transcription": False, "context_window_tokens": 128_000, "output_tokens": 8_192},
}


def recommended_models_table(task: str | None = None,
                             provider: str | None = None,
                             text_generation: bool | None = None,
                             vision: bool | None = None,
                             image_generation: bool | None = None,
                             audio_transcription: bool | None = None,
                             min_context: int | None = None,
                             min_output_tokens: int | None = None,
                             image_modification: bool | None = None) -> str:
    """Return a markdown table of recommended models filtered by capabilities."""
    if task:
        t = task.lower()
        if t in {"vision", "multimodal", "vl"} and vision is None:
            vision = True
        elif t in {"image", "image_generation", "image-generation"} and image_generation is None:
            image_generation = True
        elif t in {"image_modification", "image-edit", "image_edit", "image-editing", "editing"} and image_modification is None:
            image_modification = True
        elif t in {"audio", "speech", "audio_transcription", "stt"} and audio_transcription is None:
            audio_transcription = True
        elif t == "text" and text_generation is None:
            text_generation = True
            vision = False if vision is None else vision
            image_generation = False if image_generation is None else image_generation
            image_modification = False if image_modification is None else image_modification
            audio_transcription = False if audio_transcription is None else audio_transcription

    rows = []
    for model_name in sorted(RECOMMENDED_MODELS.keys()):
        cfg = RECOMMENDED_MODELS[model_name]
        model_provider = (cfg.get("provider") or "").lower()
        model_text = cfg.get("text_generation", False)
        model_vision = cfg.get("vision", False)
        model_image = cfg.get("image_generation", False)
        model_image_mod = cfg.get("image_modification", False)
        model_audio = cfg.get("audio_transcription", False)

        context = cfg.get("context_window_tokens")
        if context is None:
            context = cfg.get("context_window")

        max_tokens = cfg.get("output_tokens")
        if max_tokens is None:
            max_tokens = cfg.get("max_output_tokens")

        if provider and model_provider != provider.lower():
            continue
        if text_generation is not None and bool(model_text) != bool(text_generation):
            continue
        if vision is not None and bool(model_vision) != bool(vision):
            continue
        if image_generation is not None and bool(model_image) != bool(image_generation):
            continue
        if image_modification is not None and bool(model_image_mod) != bool(image_modification):
            continue
        if audio_transcription is not None and bool(model_audio) != bool(audio_transcription):
            continue
        if min_context and (context is None or (isinstance(context, int) and context < min_context)):
            continue
        if min_output_tokens and (max_tokens is None or (isinstance(max_tokens, int) and max_tokens < min_output_tokens)):
            continue

        def _fmt_num(x: Any) -> str:
            if x is None:
                return "-"
            try:
                return f"{int(x):,}"
            except Exception:
                return str(x)

        rows.append(
            f"| {model_name} | {model_provider or '-'} | {'✅' if model_text else '❌'} | "
            f"{'✅' if model_vision else '❌'} | {'✅' if model_image else '❌'} | "
            f"{'✅' if model_image_mod else '❌'} | {'✅' if model_audio else '❌'} | "
            f"{_fmt_num(context)} | {_fmt_num(max_tokens)} |"
        )

    if not rows:
        return "No models match the specified criteria."

    header = (
        "| Model | Provider | Text | Vision | Image Gen | Image Edit | Audio Transcription | Context Window | Max Output Tokens |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
    )
    table = header + "\n".join(rows)
    display(Markdown(table))
    return table

__all__ = ['RECOMMENDED_MODELS', 'recommended_models_table']