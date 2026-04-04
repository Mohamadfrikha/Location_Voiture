import os
import django

# 1️⃣ Définir le settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Location_Voiture.settings")

# 2️⃣ Initialiser Django
django.setup()

# 3️⃣ Maintenant tu peux importer tes modèles
from Client.models import Client

# 4️⃣ Créer le superuser si il n'existe pas
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