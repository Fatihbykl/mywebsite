from django.db import models
from django.contrib.auth.models import User


class kullaniciProfili(models.Model):
    profil = models.OneToOneField(User, null=True, on_delete=True)
    adsoyad = models.CharField(blank=True, max_length=30, verbose_name='İsminiz')
