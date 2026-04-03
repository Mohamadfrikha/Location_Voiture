from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
# Create your models here.
class ClientManager(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError("Email obligatoire")
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            **extra_fields
        )
        extra_fields.setdefault('is_active', False)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
class Client(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    CIN = models.CharField(max_length=20, unique=True)
    telephone = models.CharField(max_length=8, unique=True , validators=[MinLengthValidator(8)])
    date_naissance = models.DateField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='clientphoto/', default='clientphoto/photo.jpg')
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'CIN']
    objects = ClientManager()
    is_active = models.BooleanField(default=True)
    
    is_email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_validated = models.BooleanField(default=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    