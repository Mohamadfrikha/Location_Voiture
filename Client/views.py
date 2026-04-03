import random
from urllib.parse import urlencode
from django.conf import settings

from django.shortcuts import redirect, render

from django.template.loader import render_to_string

from django.urls import reverse
from SecureToken.utils import generate_secure_token, verify_secure_token
from .models import Client  
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail ,EmailMultiAlternatives
from urllib.parse import urlencode
from django.contrib import messages
from Notification.models import Notification
import traceback
def maskEmail(email):
    local, domain = email.split("@")
    masked_local = local[0] + "*" * (len(local) - 1)
    return f"{masked_local}@{domain}"

@csrf_exempt
def CreateClient(request):
    if request.method == 'POST':
        try:
            """data = json.loads(request.body)

            nom = data.get("nom")
            prenom = data.get("prenom")
            email = data.get("email")
            CIN = data.get("CIN")
            telephone = data.get("telephone", "")
            date_naissance = data.get("date_naissance", None)"""
            nom = request.POST.get("nom")
            prenom = request.POST.get("prenom")
            email = request.POST.get("email")
            CIN = request.POST.get("CIN")
            telephone = request.POST.get("telephone", "")
            date_naissance = request.POST.get("date_naissance")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, "client:client_create", {
                    "message": "Passwords do not match"
                })
            if date_naissance:
                date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d").date()
            if Client.objects.filter(telephone=telephone).exists():
                messages.error(request, "Un compte avec ce numéro de téléphone existe déjà.")
                return redirect("client:client_create")
            
            client = Client(
                nom=nom,
                prenom=prenom,
                email=email,
                CIN=CIN,
                telephone=telephone,
                date_naissance=date_naissance,
                is_active=False
            )
            client.is_active=False
            client.set_password(password)
            otp = str(random.randint(100000, 999999))
            client.otp_code = otp
            client.otp_validated = False
            client.otp_expires_at = timezone.now() + timedelta(minutes=15)
            client.save()
            TOKEN = generate_secure_token(client)
            html_content = render_to_string("Client/email/otp_email.html", {
                "user": client,
                "otp": otp
            })
            emailEnvoi= EmailMultiAlternatives(
                subject="Code de vérification",
                body=f"Votre code OTP est : {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[client.email]
            )
            emailEnvoi.attach_alternative(html_content, "text/html")
            emailEnvoi.send()
            base_url = reverse("client:verify_otp")  # هذا يرجع /clients/verify-otp/
            query_string = urlencode({"token": TOKEN})  # يحول dict لـ token=...
            url = f"{base_url}?{query_string}"
            return redirect(url)
        except Exception as e:
            print("Exception message:", e)          # الرسالة وحدها
            traceback.print_exc() 
            return render(request, 'Client/client_created.html', {
                "status": "error",
                "message": str(e)
            })

    return render(request, 'Client/client_created.html', {
                "status": "success"
            })
@csrf_exempt
def verify_otp(request):
    token = request.GET.get('token')
    client=verify_secure_token(token)
    if not client:
        return redirect('voiture:accueil')
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        try:
            client = Client.objects.get(email=client.email)
            if client.otp_code == otp_code and timezone.now() < client.otp_expires_at:
                client.otp_validated = True
                client.is_active = True
                client.save()
                
                Notification.objects.create(
                    user=client,                      
                    sujet="Bienvenue sur notre site !",
                    message="Bonjour {} ! Merci de vous être inscrit. 🎉".format(client)                     
                )
                messages.success(request, "OTP code verified successfully. Your account is now active.")
                login(request,client)
                return redirect('voiture:accueil')   
            else:
                return render(request, 'Client/verify_otp.html', {
                    "message": "Invalid or expired OTP code"
                })
        except Client.DoesNotExist:
            return render(request, 'Client/verify_otp.html', {
                "message": "Client not found"
            })
    return render(request, 'Client/verify_otp.html',{"message":"compte create avec success","mask_email":maskEmail(client.email),"email":client.email,"token":token})
@csrf_exempt
def renvoyer_otp(request):
    
    if request.method == 'POST':  
        email = request.POST.get('email')
        try:
            client = Client.objects.get(email=email)
            if not client.otp_validated:
                otp = str(random.randint(100000, 999999))
                client.otp_code = otp
                client.otp_expires_at = timezone.now() + timedelta(minutes=15)
                client.save()
                TOKEN = generate_secure_token(client)
                send_mail(
                    subject='Votre nouveau code de vérification',
                    message=f'Bonjour {client.nom} {client.prenom} ,\n\nVotre nouveau code OTP est : {otp} ',
                    from_email='mohamedfrikha65@gmail.com',
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                base_url = reverse("client:verify_otp")  # هذا يرجع /clients/verify-otp/
                query_string = urlencode({"token": TOKEN})  # يحول dict لـ token=...
                url = f"{base_url}?{query_string}"
                return redirect(url)
        except Client.DoesNotExist:
            return render(request, 'clinet:verify_otp', {
                "message": "Client not found"
            })
    return render(request, 'client:verify_otp.html')
def login_client(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        client = authenticate(request, email=email, password=password)
        if client is not None:
            login(request, client)
            return redirect('voiture:accueil')
        else:
            return render(request, 'Client/login.html', {'error': 'Email ou mot de passe incorrect'})
    return render(request, 'Client/login.html')
def logout_client(request):
    logout(request)
    return redirect('voiture:accueil')