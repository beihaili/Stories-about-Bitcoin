"""
Multi-model registry for the content pipeline.

Supports three tiers:
- budget:  Cheapest models for drafting and iteration
- default: Balanced cost/quality for production use
- premium: Best models for flagship chapters

All models route through OpenRouter API.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelConfig:
    """Configuration for a single model."""
    model_id: str
    name: str
    provider: str
    cost_per_1k_input: float   # USD per 1K input tokens
    cost_per_1k_output: float  # USD per 1K output tokens
    max_context: int           # Max context window tokens
    notes: str = ""


# Model registry
MODELS = {
    # Claude models
    "claude-opus": ModelConfig(
        model_id="anthropic/claude-opus-4",
        name="Claude Opus",
        provider="Anthropic",
        cost_per_1k_input=0.015,
        cost_per_1k_output=0.075,
        max_context=200000,
        notes="Flagship, best for creative writing",
    ),
    "claude-sonnet": ModelConfig(
        model_id="anthropic/claude-sonnet-4",
        name="Claude Sonnet",
        provider="Anthropic",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        max_context=200000,
        notes="Best balance of quality and cost",
    ),
    "claude-haiku": ModelConfig(
        model_id="anthropic/claude-haiku-4.5",
        name="Claude Haiku",
        provider="Anthropic",
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.005,
        max_context=200000,
        notes="Fast and cheap, good for scoring",
    ),
    # GPT models
    "gpt-4o": ModelConfig(
        model_id="openai/gpt-4o",
        name="GPT-4o",
        provider="OpenAI",
        cost_per_1k_input=0.0025,
        cost_per_1k_output=0.01,
        max_context=128000,
        notes="Strong all-rounder",
    ),
    "gpt-4o-mini": ModelConfig(
        model_id="openai/gpt-4o-mini",
        name="GPT-4o Mini",
        provider="OpenAI",
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        max_context=128000,
        notes="Very cheap, good for summarization",
    ),
    # Gemini models
    "gemini-flash": ModelConfig(
        model_id="google/gemini-2.0-flash-001",
        name="Gemini 2.0 Flash",
        provider="Google",
        cost_per_1k_input=0.0001,
        cost_per_1k_output=0.0004,
        max_context=1000000,
        notes="Extremely fast and cheap, great for translation",
    ),
    "gemini-pro": ModelConfig(
        model_id="google/gemini-2.5-pro-preview",
        name="Gemini 2.5 Pro",
        provider="Google",
        cost_per_1k_input=0.00125,
        cost_per_1k_output=0.01,
        max_context=1000000,
        notes="Strong reasoning, huge context",
    ),
    # DeepSeek
    "deepseek-v3": ModelConfig(
        model_id="deepseek/deepseek-chat",
        name="DeepSeek V3",
        provider="DeepSeek",
        cost_per_1k_input=0.00014,
        cost_per_1k_output=0.00028,
        max_context=64000,
        notes="Very cheap, strong Chinese",
    ),
}


@dataclass
class TierConfig:
    """Model assignments for each role in a tier."""
    director: str    # Model key for StoryDirector (planning)
    writer: str      # Model key for MingWriter (drafting)
    scorer: str      # Model key for QualityScorer
    translator: str  # Model key for Translator
    summarizer: str  # Model key for ChunkSummarizer


# Tier definitions
TIERS: Dict[str, TierConfig] = {
    "budget": TierConfig(
        director="gpt-4o-mini",
        writer="deepseek-v3",
        scorer="claude-haiku",
        translator="gemini-flash",
        summarizer="gpt-4o-mini",
    ),
    "default": TierConfig(
        director="claude-sonnet",
        writer="claude-sonnet",
        scorer="claude-haiku",
        translator="gemini-flash",
        summarizer="gpt-4o-mini",
    ),
    "premium": TierConfig(
        director="claude-sonnet",
        writer="claude-opus",
        scorer="claude-sonnet",
        translator="gemini-pro",
        summarizer="claude-haiku",
    ),
}


def get_tier(name: str) -> TierConfig:
    """Get a tier config by name."""
    if name not in TIERS:
        raise ValueError(f"Unknown tier '{name}'. Choose from: {list(TIERS.keys())}")
    return TIERS[name]


def get_model(key: str) -> ModelConfig:
    """Get a model config by key."""
    if key not in MODELS:
        raise ValueError(f"Unknown model '{key}'. Choose from: {list(MODELS.keys())}")
    return MODELS[key]


def get_model_id(key: str) -> str:
    """Get the OpenRouter model ID for a model key."""
    return get_model(key).model_id


def resolve_tier_models(tier_name: str) -> Dict[str, str]:
    """Resolve a tier to a dict of role -> OpenRouter model ID."""
    tier = get_tier(tier_name)
    return {
        "director": get_model_id(tier.director),
        "writer": get_model_id(tier.writer),
        "scorer": get_model_id(tier.scorer),
        "translator": get_model_id(tier.translator),
        "summarizer": get_model_id(tier.summarizer),
    }


def estimate_cost(tier_name: str, input_tokens: int, output_tokens: int) -> Dict[str, float]:
    """Estimate cost for a full pipeline run at given tier."""
    tier = get_tier(tier_name)
    costs = {}
    for role in ("director", "writer", "scorer", "translator"):
        model_key = getattr(tier, role)
        model = get_model(model_key)
        cost = (
            (input_tokens / 1000) * model.cost_per_1k_input
            + (output_tokens / 1000) * model.cost_per_1k_output
        )
        costs[role] = round(cost, 4)
    costs["total"] = round(sum(costs.values()), 4)
    return costs


def list_models():
    """Print all available models."""
    print(f"{'Key':<16} {'Name':<20} {'Provider':<10} {'In/1K':<8} {'Out/1K':<8} {'Notes'}")
    print("-" * 90)
    for key, m in MODELS.items():
        print(
            f"{key:<16} {m.name:<20} {m.provider:<10} "
            f"${m.cost_per_1k_input:<7.4f} ${m.cost_per_1k_output:<7.4f} {m.notes}"
        )


def list_tiers():
    """Print all available tiers."""
    for name, tier in TIERS.items():
        models = resolve_tier_models(name)
        est = estimate_cost(name, 10000, 4000)
        print(f"\n[{name.upper()}] (~${est['total']:.2f} per chapter)")
        for role, model_id in models.items():
            print(f"  {role:<12} {model_id}")
