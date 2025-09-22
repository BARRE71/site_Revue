from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from core.models import TimeStampedModel


class UserProfile(TimeStampedModel):
    """Modèle pour étendre le profil utilisateur"""
    
    ROLE_CHOICES = [
        ('normal', 'Utilisateur normal'),
        ('subscriber', 'Abonné'),
        ('admin', 'Administrateur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Utilisateur")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    country = CountryField(blank=True, verbose_name="Pays")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    address = models.TextField(blank=True, verbose_name="Adresse")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Photo de profil")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal', verbose_name="Rôle utilisateur")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    website = models.URLField(blank=True, verbose_name="Site web")
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
