from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from core.models import TimeStampedModel


class SubscriptionPlan(TimeStampedModel):
    """Modèle pour les plans d'abonnement"""
    
    PLAN_TYPE_CHOICES = [
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom du plan")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, verbose_name="Type de plan")
    duration_days = models.PositiveIntegerField(verbose_name="Durée en jours")
    features = models.JSONField(default=list, verbose_name="Fonctionnalités incluses")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_popular = models.BooleanField(default=False, verbose_name="Plan populaire")
    
    class Meta:
        verbose_name = "Plan d'abonnement"
        verbose_name_plural = "Plans d'abonnement"
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - {self.get_plan_type_display()}"


class Subscription(TimeStampedModel):
    """Modèle pour les abonnements actifs des utilisateurs"""
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('expired', 'Expiré'),
        ('cancelled', 'Annulé'),
        ('suspended', 'Suspendu'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name="Plan")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Statut")
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    auto_renew = models.BooleanField(default=True, verbose_name="Renouvellement automatique")
    stripe_subscription_id = models.CharField(max_length=100, blank=True, verbose_name="ID Stripe")
    
    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Abonnement de {self.user.username} - {self.plan.name}"
    
    @property
    def is_active(self):
        from django.utils import timezone
        return self.status == 'active' and timezone.now() <= self.end_date


class PaymentHistory(TimeStampedModel):
    """Modèle pour l'historique des paiements"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name="Abonnement")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    currency = models.CharField(max_length=3, default='EUR', verbose_name="Devise")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    payment_method = models.CharField(max_length=50, verbose_name="Méthode de paiement")
    stripe_payment_id = models.CharField(max_length=100, blank=True, verbose_name="ID Paiement Stripe")
    transaction_date = models.DateTimeField(verbose_name="Date de transaction")
    
    class Meta:
        verbose_name = "Historique des paiements"
        verbose_name_plural = "Historique des paiements"
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"Paiement {self.stripe_payment_id} - {self.user.username}"


class NewsletterSubscription(TimeStampedModel):
    """Modèle pour les abonnements à la newsletter"""
    
    email = models.EmailField(unique=True, verbose_name="Email")
    domains = models.TextField(blank=True, verbose_name="Domaines d'intérêt")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    
    class Meta:
        verbose_name = "Abonnement newsletter"
        verbose_name_plural = "Abonnements newsletter"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
