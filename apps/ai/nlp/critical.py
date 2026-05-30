"""
Détection de signaux critiques (mots‑clés et patterns) dans le texte.
Ne pose jamais de diagnostic médical.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Patterns pour différents niveaux d'alerte
CRITICAL_PATTERNS = {
    "suicidal_ideation": [
        r"\b(kill\s*myself|end\s*my\s*life|suicide|want\s*to\s*die|no\s*reason\s*to\s*live)\b",
    ],
    "severe_anxiety": [
        r"\b(can'?t\s*breathe|panic\s*attack|overwhelmed\s*by\s*fear)\b",
    ],
    "burnout": [
        r"\b(exhausted|burned?\s*out|no\s*energy|can'?t\s*go\s*on)\b",
    ],
}


def detect_critical_signals(text: str) -> list[str]:
    """
    Analyse le texte à la recherche de signaux critiques prédéfinis.

    Args:
        text: Texte libre à analyser.

    Returns:
        Liste de flags (ex: 'suicidal_ideation', 'severe_anxiety', 'burnout').
        Liste vide si rien n'est détecté.
    """
    if not text or not text.strip():
        return []

    text_lower = text.lower()
    flags = []

    for flag, patterns in CRITICAL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                flags.append(flag)
                break  # un seul motif suffit pour lever le flag

    if flags:
        logger.info(f"Critical signals detected: {flags}")

    return flags