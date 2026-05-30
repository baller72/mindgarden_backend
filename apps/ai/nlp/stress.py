"""
Détection des scores émotionnels fins : stress, tristesse, anxiété, positivité.
Utilise un modèle DistilRoBERTa fine-tuné sur les émotions.
"""

import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

_emotion_pipeline = None


def _load_emotion_pipeline():
    """Charge le pipeline de classification d'émotions une seule fois."""
    global _emotion_pipeline
    if _emotion_pipeline is None:
        try:
            _emotion_pipeline = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True,
            )
            logger.info("Emotion pipeline loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load emotion pipeline: {e}")
    return _emotion_pipeline


def detect_stress(text: str) -> dict[str, int]:
    """
    Extrait les scores d'émotions (0 à 100) à partir du texte.

    Returns:
        dict avec les clés 'stress', 'sadness', 'anxiety', 'positivity'.
        Chaque valeur est un entier entre 0 et 100.
    """
    scores = {"stress": 0, "sadness": 0, "anxiety": 0, "positivity": 0}
    if not text or not text.strip():
        return scores

    pipe = _load_emotion_pipeline()
    if pipe is None:
        return scores

    try:
        truncated_text = text[:512]
        emotions = pipe(truncated_text)[0]
    except Exception as e:
        logger.warning(f"Emotion detection failed: {e}")
        return scores

    # Mapping du modèle vers nos catégories
    label_mapping = {
        "anger": "stress",
        "disgust": "stress",
        "fear": "anxiety",
        "sadness": "sadness",
        "joy": "positivity",
        "surprise": "positivity",  # surprise neutre/positif
    }

    for emo in emotions:
        label = emo["label"]
        score = emo["score"]
        if label in label_mapping:
            key = label_mapping[label]
            # Conversion en pourcentage (0-100) et on garde le score max
            scores[key] = max(scores[key], int(score * 100))

    return scores