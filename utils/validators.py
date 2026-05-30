import re

def validate_text(text: str) -> str:
    """Nettoie et valide un texte."""
    if not text:
        return ""
    # Supprimer les caractères non imprimables sauf ponctuation
    text = re.sub(r'[^\x20-\x7E]', '', text)
    return text.strip()[:5000]  # limite de longueur