from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Location
from Notification.models import Notification

def accepter_location_admin(location_id):
    loc = get_object_or_404(Location, id=location_id)
    
    loc.decision = "AC"  # ACCEPTÉE
    loc.save()

    # Crée la notification interne
    Notification.objects.create(
        user=loc.client,  # si Client a un champ user
        message=f"Votre location de {loc.voiture} a été acceptée par l'administrateur."
    )

    # Prépare l'email
    html_content = render_to_string("Location/email/acceptation.html", {
        "location": loc,
    })
    email = EmailMultiAlternatives(
        subject="Votre réservation a été acceptée !",
        body=f"Bonjour {loc.client},\nVotre réservation pour la voiture {loc.voiture} a été acceptée.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[loc.client.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()