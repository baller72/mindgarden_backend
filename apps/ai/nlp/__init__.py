"""
Module NLP pour MindGarden – analyse des émotions, stress, signaux critiques.
Expose des fonctions simples utilisées par apps.ai.services.
"""

from .sentiment import analyze_sentiment
from .stress import detect_stress
from .critical import detect_critical_signals

__all__ = [
    "analyze_sentiment",
    "detect_stress",
    "detect_critical_signals",
]