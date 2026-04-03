from datetime import timedelta
from django.utils import timezone
from .models import SecureToken

def generate_secure_token(user):
    expires = timezone.now() + timedelta(minutes=15)  # expiration 15 min
    token = SecureToken.objects.create(user=user, expires_at=expires)
    return token.token

def verify_secure_token(token_str):
    try:
        token = SecureToken.objects.get(token=token_str)
    except SecureToken.DoesNotExist:
        return None

    if token.is_valid():
        token.nb_used += 1
        
        
        if token.nb_used>=2:
            token.used=True
        token.save()
        return token.user
    return None