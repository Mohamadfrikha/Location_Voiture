from django.urls import path
from . import views
app_name = 'client'
urlpatterns = [
    path('create/', views.CreateClient, name='client_create'),
    path('login/', views.login_client, name='client_login'),
    path('logout/', views.logout_client, name='client_logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('renvoyer-otp/', views.renvoyer_otp, name='renvoyer_otp'),
]