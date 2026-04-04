# Image de base Python
FROM python:3.12-slim
# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1
# Répertoire de travail
WORKDIR /app
# Installer les dépendances système
RUN apt-get update && apt-get install -y \
build-essential \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*
# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
# Copier le code source
COPY . .
# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python create_superuser.py && \
    gunicorn Location_Voiture.wsgi:application --bind 0.0.0.0:$PORT