from Client.models import Client  # ou le chemin correct de ton app
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Location_Voiture.settings")
django.setup()

if not Client.objects.filter(email="mohamedfrikha65@gmail.com").exists():
    Client.objects.create_superuser(
        email="mohamedfrikha65@gmail.com",
        password="123456",
        nom="frikha",
        prenom="mohamed",
        CIN="00000000"
    )
    print("Superuser créé !")
else:
    print("Superuser existe déjà.")