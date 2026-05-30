from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def get_tokens_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def blacklist_token(token: str) -> None:
    try:
        token_obj = RefreshToken(token)
        token_obj.blacklist()
    except Exception:
        pass