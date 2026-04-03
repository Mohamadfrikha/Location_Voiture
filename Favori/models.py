from django.db import models
from Client.models import Client

class Favori(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='favoris')
    voiture = models.ForeignKey("Voiture.Voiture", on_delete=models.CASCADE,related_name='favoris')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'voiture')  # يمنع doublon

    def __str__(self):
        return f"{self.user} -Favori- {self.voiture}"