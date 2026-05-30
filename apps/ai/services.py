import whisper
import spacy
from transformers import pipeline
from typing import Dict, Any, List
from utils.validators import validate_text
import logging

logger = logging.getLogger(__name__)

# Charger les modèles une fois
try:
    whisper_model = whisper.load_model("base")
except Exception as e:
    logger.error(f"Whisper loading failed: {e}")
    whisper_model = None

try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

try:
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
except Exception as e:
    logger.error(f"Transformers loading failed: {e}")
    sentiment_pipeline = None
    emotion_pipeline = None

def transcribe_audio(file_path: str) -> str:
    """Transcrit un fichier audio avec Whisper."""
    if not whisper_model:
        return "Whisper model unavailable"
    result = whisper_model.transcribe(file_path)
    return result['text'].strip()

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyse un texte pour en extraire:
    - sentiment (positif/négatif)
    - scores émotionnels (stress, tristesse, anxiété, positivité)
    - détection de signaux critiques
    - recommandation
    Retourne un dict compatible avec le modèle EmotionAnalysis.
    """
    if not text:
        return {}
    text = validate_text(text)
    result = {
        "emotion": "neutral",
        "stress_score": 0,
        "sentiment_score": 0.5,
        "sadness": 0,
        "anxiety": 0,
        "positivity": 0,
        "recommendation": "",
        "critical_flags": []
    }

    # Sentiment global
    if sentiment_pipeline:
        try:
            sent = sentiment_pipeline(text[:512])[0]  # limitation longueur
            label = sent['label']
            score = sent['score']
            if label == 'POSITIVE':
                result['sentiment_score'] = 0.5 + (score / 2)
                result['positivity'] = int(score * 100)
            else:
                result['sentiment_score'] = 0.5 - (score / 2)
                result['sadness'] = int(score * 50)
                result['anxiety'] = int(score * 50)
        except Exception as e:
            logger.warning(f"Sentiment analysis error: {e}")

    # Emotions détaillées
    if emotion_pipeline:
        try:
            emotions = emotion_pipeline(text[:512])[0]
            # mapping des labels: anger, disgust, fear, joy, neutral, sadness, surprise
            for emo in emotions:
                label = emo['label']
                score = emo['score']
                if label == 'sadness':
                    result['sadness'] = max(result['sadness'], int(score*100))
                elif label == 'fear':
                    result['anxiety'] = max(result['anxiety'], int(score*100))
                elif label == 'joy':
                    result['positivity'] = max(result['positivity'], int(score*100))
                elif label == 'anger':
                    result['stress_score'] = max(result['stress_score'], int(score*70))
                elif label == 'disgust':
                    result['stress_score'] = max(result['stress_score'], int(score*50))
        except Exception as e:
            logger.warning(f"Emotion analysis error: {e}")

    # Calcul du stress score combiné (0-100)
    result['stress_score'] = max(result['stress_score'], 
                                 int((result['anxiety'] + result['sadness']) / 2))
    # Normaliser
    result['stress_score'] = min(100, result['stress_score'])
    result['sadness'] = min(100, result['sadness'])
    result['anxiety'] = min(100, result['anxiety'])
    result['positivity'] = min(100, result['positivity'])

    # Détection de signaux critiques (mots-clés simples)
    critical_keywords = ['suicide', 'kill myself', 'end my life', 'die', 'harm myself']
    if any(word in text.lower() for word in critical_keywords):
        result['critical_flags'].append('suicidal_ideation')
    # Stress très élevé
    if result['stress_score'] > 80:
        result['critical_flags'].append('high_stress')
    # Anxiété sévère
    if result['anxiety'] > 85:
        result['critical_flags'].append('severe_anxiety')

    # Recommandation
    if result['stress_score'] > 70 or result['anxiety'] > 70:
        result['recommendation'] = 'breathing_exercise'
        result['emotion'] = 'anxiety'
    elif result['sadness'] > 70:
        result['recommendation'] = 'journaling_prompt'
        result['emotion'] = 'sadness'
    elif result['positivity'] > 70:
        result['emotion'] = 'positive'
    else:
        result['emotion'] = 'neutral'

    return result

# Service additionnel pour les insights (utilisé par l'app insights)
def aggregate_emotions(analyses):
    """Calcule les moyennes à partir d'un queryset d'EmotionAnalysis."""
    if not analyses:
        return {}
    count = len(analyses)
    avg_stress = sum(a.stress_score for a in analyses) / count
    avg_sadness = sum(a.sadness_score for a in analyses) / count
    avg_anxiety = sum(a.anxiety_score for a in analyses) / count
    avg_positivity = sum(a.positivity_score for a in analyses) / count
    return {
        'avg_stress': round(avg_stress, 1),
        'avg_sadness': round(avg_sadness, 1),
        'avg_anxiety': round(avg_anxiety, 1),
        'avg_positivity': round(avg_positivity, 1),
        'count': count
    }