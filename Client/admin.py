from django.contrib import admin
from .models import Client
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(Client)
class ClientAdmin(UserAdmin):
    model = Client
    list_display = ('email', 'nom', 'prenom', 'is_staff', 'is_active', 'is_superuser')  # utilise les vrais champs du modèle
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # utilise les vrais champs du modèle
    ordering = ('email',)  # ne pas mettre 'username'
    search_fields = ('email', 'nom', 'prenom')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nom', 'prenom', 'telephone', 'CIN', 'date_naissance','photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser','is_active','otp_validated', 'groups', 'user_permissions')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )