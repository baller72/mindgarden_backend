from .models import JournalEntry
from apps.ai.services import analyze_text, transcribe_audio
from celery import shared_task

@shared_task
def process_journal_entry(entry_id: int):
    try:
        entry = JournalEntry.objects.get(id=entry_id)
        # Transcription si audio
        if entry.audio_file and not entry.transcription:
            text = transcribe_audio(entry.audio_file.path)
            entry.transcription = text
            entry.text = text  # ou concaténer avec texte existant
        # Analyse IA
        text_to_analyze = entry.text or entry.transcription
        if text_to_analyze:
            analysis = analyze_text(text_to_analyze)
            entry.mood = analysis.get('emotion', '')
            entry.stress_score = analysis.get('stress_score')
            entry.sentiment_score = analysis.get('sentiment_score')
            # Sauvegarder l'analyse émotionnelle détaillée dans EmotionAnalysis
            from apps.emotions.models import EmotionAnalysis
            EmotionAnalysis.objects.create(
                user=entry.user,
                journal_entry=entry,
                stress_score=analysis.get('stress_score', 0),
                sadness_score=analysis.get('sadness', 0),
                anxiety_score=analysis.get('anxiety', 0),
                positivity_score=analysis.get('positivity', 0),
                emotion=analysis.get('emotion', ''),
                recommendation=analysis.get('recommendation', ''),
                critical_flags=analysis.get('critical_flags', [])
            )
        entry.save()
    except JournalEntry.DoesNotExist:
        pass