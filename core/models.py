from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django_countries.fields import CountryField


class TimeStampedModel(models.Model):
    """Modèle de base avec timestamps automatiques"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))

    class Meta:
        abstract = True


class Contact(TimeStampedModel):
    """Modèle pour les messages de contact"""
    name = models.CharField(max_length=100, verbose_name=_("Nom complet"))
    email = models.EmailField(verbose_name=_("Adresse email"))
    subject = models.CharField(max_length=200, verbose_name=_("Sujet"))
    message = models.TextField(verbose_name=_("Message"))
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name=_("Téléphone"),
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_("Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés.")
            )
        ]
    )
    country = CountryField(blank=True, verbose_name=_("Pays"))
    city = models.CharField(max_length=100, blank=True, verbose_name=_("Ville"))
    address = models.TextField(blank=True, verbose_name=_("Adresse complète"))
    is_read = models.BooleanField(default=False, verbose_name=_("Message lu"))
    response = models.TextField(blank=True, verbose_name=_("Réponse"))

    class Meta:
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%d/%m/%Y')})"


class Newsletter(TimeStampedModel):
    """Modèle pour les newsletters"""
    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    content = models.TextField(verbose_name=_("Contenu"))
    is_sent = models.BooleanField(default=False, verbose_name=_("Newsletter envoyée"))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Date d'envoi"))
    subscribers_count = models.PositiveIntegerField(default=0, verbose_name=_("Nombre d'abonnés"))

    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SiteSettings(TimeStampedModel):
    """Modèle pour les paramètres du site"""
    site_name = models.CharField(max_length=100, default="RevueMaroc", verbose_name=_("Nom du site"))
    site_description = models.TextField(blank=True, verbose_name=_("Description du site"))
    contact_email = models.EmailField(blank=True, verbose_name=_("Email de contact"))
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name=_("Téléphone de contact"))
    address = models.TextField(blank=True, verbose_name=_("Adresse"))
    facebook_url = models.URLField(blank=True, verbose_name=_("URL Facebook"))
    twitter_url = models.URLField(blank=True, verbose_name=_("URL Twitter"))
    linkedin_url = models.URLField(blank=True, verbose_name=_("URL LinkedIn"))
    instagram_url = models.URLField(blank=True, verbose_name=_("URL Instagram"))
    logo = models.ImageField(upload_to='site/', blank=True, verbose_name=_("Logo du site"))
    favicon = models.ImageField(upload_to='site/', blank=True, verbose_name=_("Favicon"))
    
    # Configuration des abonnements
    monthly_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=9.99,
        verbose_name=_("Prix mensuel (€)")
    )
    yearly_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=99.99,
        verbose_name=_("Prix annuel (€)")
    )
    
    # Configuration des livres
    shipping_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=5.99,
        verbose_name=_("Frais de livraison (€)")
    )
    free_shipping_threshold = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=50.00,
        verbose_name=_("Seuil livraison gratuite (€)")
    )

    class Meta:
        verbose_name = _("Paramètre du site")
        verbose_name_plural = _("Paramètres du site")

    def __str__(self):
        return f"Paramètres de {self.site_name}"

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule instance
        if not self.pk and SiteSettings.objects.exists():
            return
        super().save(*args, **kwargs)


class Category(TimeStampedModel):
    """Modèle pour les catégories générales"""
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name=_("Image"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre d'affichage"))

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/categories/{self.slug}/'


class Tag(TimeStampedModel):
    """Modèle pour les tags"""
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Nom"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    color = models.CharField(max_length=7, default="#007bff", verbose_name=_("Couleur"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']

    def __str__(self):
        return self.name
