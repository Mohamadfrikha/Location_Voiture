from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
from Client.models import Client

class SecureToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    nb_used=models.IntegerField(default=0)
    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at and self.nb_used < 2
    def __str__(self):
        return f"{self.user.email} - {self.token}"