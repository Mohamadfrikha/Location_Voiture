
from Client.models import Client
from .utils import generate_secure_token
from django.shortcuts import render

# Create your views here.

def create_secure_token(request, email):
    try:
        client= Client.objects.get(email=email)
    except Client.DoesNotExist:
        return render(request, "Client/client_error.html", {"message": "Client non trouvé"}, status=404)

    token = generate_secure_token(client)
    
    # Retourne l’URL sécurisée à utiliser
    secure_url = f"http://localhost:5173/verifier-code/{token}"
    return secure_url,token
