from django.db import models
from Client.models import Client

class Notification(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.sujet}"