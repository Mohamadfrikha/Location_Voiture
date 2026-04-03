from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Location,Decision
from Voiture.models import  Voiture
from django.contrib import messages
from datetime import datetime,date
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from Notification.models import Notification
from django.core.paginator import Paginator
# Create your views here.
@login_required(login_url='client:client_login')
def louer_voiture(request,id_voiture):
    
    voiture = get_object_or_404(Voiture, id=id_voiture)
    locations = Location.objects.filter(voiture=voiture)
    dates_reservees = []
    for loc in locations:
        dates_reservees.append({
            "from": loc.date_debut.strftime("%Y-%m-%d"),
            "to": loc.date_fin.strftime("%Y-%m-%d"),
    })

    if request.method == "POST":
        date_debut_str = request.POST.get("date_debut")
        date_fin_str = request.POST.get("date_fin")

        if date_debut_str and date_fin_str:
            # convertir les dates en datetime.date
            date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
            date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

            # Vérifier que la date de fin est après la date de début
            if date_debut < date.today():
                messages.error(request, "La date de début doit être aujourd'hui ou plus tard.")
            elif date_fin < date_debut:
                messages.error(request, "La date de fin doit être après la date de début.")
            else:
                # Vérifier si la voiture est déjà louée sur cette période
                conflit = Location.objects.filter(
                    voiture=voiture,
                    est_active=True,
                    date_debut__lte=date_fin,
                    date_fin__gte=date_debut
                ).exists()
                if conflit:
                    messages.error(request, "La voiture est déjà louée pour cette période.")
                else:
                    location = Location(
                        voiture=voiture,
                        client=request.user,
                        date_debut=date_debut,
                        date_fin=date_fin
                    )
                    location.save()
                    
                    html_content = render_to_string("Location/email/create_location_success.html", {
                        "location": location,
                        "user": location.client
                    })
                    emailEnvoi= EmailMultiAlternatives(
                        subject=f"Votre location pour {location.voiture} a été créée !",
                        body=f"Bonjour {location.client}, votre location a été créée avec succès.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[location.client.email]
                    )
                    emailEnvoi.attach_alternative(html_content, "text/html")
                    emailEnvoi.send()
                    Notification.objects.create(
                        user=location.client,
                        sujet="Votre location a été créée",
                        message=f"Votre location pour {location.voiture} a été créée avec succès. Elle est en attente de validation par l’administrateur."
                    )
                    messages.success(request, "Votre location a été enregistrée avec succès.")
                    
                    return redirect('location:mes_locations')
    context = {
        "voiture": voiture,
        "dates_reservees": json.dumps(dates_reservees)
    }
    return render(request, "Location/louer_voiture.html", context)
@login_required(login_url='client:client_login')
def mes_locations(request):
    
    client_user = request.user

    # Locations terminées
    V_location_terminer = Location.objects.select_related(
        'voiture','voiture__modele','voiture__modele__marque'
    ).filter(
        est_terminer=True,
        client=client_user
    ).order_by('-date_creation')
    
    page = request.GET.get('page', 1)  # numéro de page depuis l'URL, défaut = 1
    paginator = Paginator(V_location_terminer, 5)
    page_obj_location_terminer = paginator.get_page(page)

    # Locations actives
    V_location_active = Location.objects.select_related(
        'voiture','voiture__modele','voiture__modele__marque'
    ).filter(
        est_active=True,
        client=client_user
    ).order_by('-date_creation')

    # Locations en attente ou filtrées par décision
    V_location = Location.objects.select_related(
        'voiture','voiture__modele','voiture__modele__marque'
    ).filter(
        est_active=False,
        est_terminer=False,
        client=client_user
    )
    V_location_en = V_location.filter(decision=Decision.EN_ATTENTE).order_by('-date_creation')
    V_location_ac = V_location.filter(decision=Decision.ACCEPTEE).order_by('-date_creation')
    V_location_rf = V_location.filter(decision=Decision.REFUSEE).order_by('-date_creation')

    context = {
        "V_location_active": V_location_active,
        "V_location_terminer": page_obj_location_terminer,
        "V_location_en": V_location_en,
        "V_location_ac": V_location_ac,
        "V_location_rf": V_location_rf,
    }

    return render(request, "Location/mes_locations.html", context)
    