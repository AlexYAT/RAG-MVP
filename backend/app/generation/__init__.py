"""Grounded generation on top of retrieval baseline."""

from app.generation.answer import generate_from_hits
from app.generation.pipeline import run_generation_answer

__all__ = ["generate_from_hits", "run_generation_answer"]
