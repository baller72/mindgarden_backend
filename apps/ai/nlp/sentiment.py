"""
Analyse de sentiment globale (positif / négatif) avec DistilBERT.
"""

import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

# Cache du pipeline pour éviter de recharger le modèle à chaque appel
_sentiment_pipeline = None


def _load_sentiment_pipeline():
    """Charge le pipeline de sentiment une seule fois."""
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        try:
            _sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
            )
            logger.info("Sentiment pipeline loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load sentiment pipeline: {e}")
    return _sentiment_pipeline


def analyze_sentiment(text: str) -> dict | None:
    """
    Analyse le sentiment d'un texte.

    Args:
        text: Texte à analyser (max 512 tokens seront utilisés).

    Returns:
        dict avec 'label' ('POSITIVE' ou 'NEGATIVE') et 'score' (float),
        ou None si le modèle n'est pas disponible.
    """
    if not text or not text.strip():
        return None

    pipe = _load_sentiment_pipeline()
    if pipe is None:
        return None

    try:
        # Limiter la longueur pour respecter le modèle
        truncated_text = text[:512]
        result = pipe(truncated_text)[0]
        return {"label": result["label"], "score": result["score"]}
    except Exception as e:
        logger.warning(f"Sentiment analysis failed: {e}")
        return None