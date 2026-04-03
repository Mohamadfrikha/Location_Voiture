from django.http import JsonResponse
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render ,get_object_or_404
from django.urls import reverse
from Location.models import Location

from Notification.models import Notification
from django.contrib import messages
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.template.loader import render_to_string
@csrf_exempt
def create_checkout_session(request, loc_id):
    loc = get_object_or_404(Location, id=loc_id)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',  # ← changer ici
                'product_data': {
                    'name': f'Location {loc.voiture}',
                },
                'unit_amount': int(loc.montant_a_payer_usd * 100),  # Stripe prend des cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('payments:stripe-success', kwargs={'id_loc': loc.id})),
        cancel_url = request.build_absolute_uri(reverse('payments:stripe-cancel'))
    )
    return redirect(session.url)
def stripe_success(request, id_loc):
    """
    Gère automatiquement le succès du paiement :
    - Si le paiement partiel n'est pas encore fait → il devient partiel
    - Sinon → paiement total
    """
    loc = get_object_or_404(Location, id=id_loc)

    # Déterminer automatiquement le type de paiement
    if not loc.paiement_partiel_effectue:
        loc.paiement_partiel_effectue = True
        montant_txt = "partiel"
    else:
        loc.paiement_total_effectue = True
        montant_txt = "total"

    loc.save()

    # Créer la notification
    Notification.objects.create(
        user=loc.client,
        message=f"Le paiement {montant_txt} pour la location {loc.voiture} a été effectué avec succès."
    )

    # Envoyer l'email
    html_content = render_to_string("payments/email/success.html", {"location": loc, "type_paiement": montant_txt})
    email = EmailMultiAlternatives(
        subject=f"Paiement {montant_txt} réussi - Location Voiture",
        body=f"Votre paiement {montant_txt} a été effectué avec succès.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[loc.client.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    # Message flash
    messages.success(request, f"Votre paiement {montant_txt} a été effectué avec succès !")
    
    return render(request, "payments/success.html", {"location": loc, "type_paiement": montant_txt})
def stripe_cancel(request):
    return render(request, "payments/cancel.html")