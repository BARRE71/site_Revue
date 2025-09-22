from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField
from core.models import TimeStampedModel, Category, Tag
from django.utils import timezone


class RevueCategory(Category):
    """Catégorie spécifique aux revues (proxy model)"""
    
    class Meta:
        proxy = True
        verbose_name = "Catégorie de revue"
        verbose_name_plural = "Catégories de revues"


class Author(TimeStampedModel):
    """Modèle pour les auteurs d'articles de revue"""
    
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    photo = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name="Photo")
    country = CountryField(blank=True, verbose_name="Pays")
    website = models.URLField(blank=True, verbose_name="Site web")
    is_featured = models.BooleanField(default=False, verbose_name="Auteur en vedette")
    academic_title = models.CharField(max_length=100, blank=True, verbose_name="Titre académique")
    institution = models.CharField(max_length=200, blank=True, verbose_name="Institution")
    
    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Revue(TimeStampedModel):
    """Modèle pour les numéros de revue intellectuelle"""
    
    FORMAT_CHOICES = [
        ('papier', 'Format papier'),
        ('pdf', 'Format PDF'),
        ('both', 'Les deux formats'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
        ('out_of_stock', 'Épuisé'),
    ]
    
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('ar', 'Arabe'),
        ('en', 'Anglais'),
    ]
    
    # Informations de base
    numero = models.PositiveIntegerField(unique=True, verbose_name="Numéro de la revue")
    title = models.CharField(max_length=200, verbose_name="Titre/Thème")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    
    # Contenu
    description = models.TextField(verbose_name="Description/Résumé")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="Extrait")
    editorial = models.TextField(blank=True, verbose_name="Éditorial")
    
    # Métadonnées
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr', verbose_name="Langue principale")
    pages_count = models.PositiveIntegerField(verbose_name="Nombre de pages")
    dimensions = models.CharField(max_length=50, blank=True, verbose_name="Dimensions (ex: 21x29.7 cm)")
    isbn = models.CharField(max_length=20, blank=True, verbose_name="ISBN")
    issn = models.CharField(max_length=20, blank=True, verbose_name="ISSN")
    
    # Publication
    publication_date = models.DateField(verbose_name="Date de publication")
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='both', verbose_name="Format disponible")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    
    # Prix et stock
    price_paper = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix format papier")
    price_pdf = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix format PDF")
    stock_paper = models.PositiveIntegerField(default=0, verbose_name="Stock papier")
    stock_pdf = models.PositiveIntegerField(default=0, verbose_name="Stock PDF")
    
    # Marketing
    is_featured = models.BooleanField(default=False, verbose_name="Numéro en vedette")
    is_bestseller = models.BooleanField(default=False, verbose_name="Meilleure vente")
    cover_image = models.ImageField(upload_to='revues/', blank=True, null=True, verbose_name="Image de couverture")
    pdf_file = models.FileField(upload_to='revues_pdf/', blank=True, null=True, verbose_name="Fichier PDF")
    
    # Statistiques
    sales_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de ventes")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name="Note moyenne")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")
    downloads_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de téléchargements")
    
    # Relations
    category = models.ForeignKey(RevueCategory, on_delete=models.CASCADE, verbose_name="Catégorie")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    
    class Meta:
        verbose_name = "Revue"
        verbose_name_plural = "Revues"
        ordering = ['-numero']
    
    def __str__(self):
        return f"Délibérée n°{self.numero}: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"deliberee-{self.numero}-{self.title}")
        super().save(*args, **kwargs)
    
    @property
    def is_available_paper(self):
        return self.stock_paper > 0 and self.format in ['papier', 'both']
    
    @property
    def is_available_pdf(self):
        return self.format in ['pdf', 'both']
    
    @property
    def main_price(self):
        """Prix principal affiché (papier en priorité)"""
        if self.is_available_paper:
            return self.price_paper
        return self.price_pdf


class RevueArticle(TimeStampedModel):
    """Modèle pour les articles individuels dans une revue"""
    
    title = models.CharField(max_length=200, verbose_name="Titre de l'article")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    abstract = models.TextField(verbose_name="Résumé")
    content = models.TextField(verbose_name="Contenu")
    keywords = models.CharField(max_length=300, blank=True, verbose_name="Mots-clés")
    page_start = models.PositiveIntegerField(verbose_name="Page de début")
    page_end = models.PositiveIntegerField(verbose_name="Page de fin")
    
    # Relations
    revue = models.ForeignKey(Revue, on_delete=models.CASCADE, related_name='articles', verbose_name="Revue")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Auteur")
    tags = models.ManyToManyField(Tag, blank=True, related_name='revue_articles', verbose_name="Tags")
    
    class Meta:
        verbose_name = "Article de revue"
        verbose_name_plural = "Articles de revue"
        ordering = ['page_start']
    
    def __str__(self):
        return f"{self.title} - {self.revue}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Générer un slug basé sur le titre
            base_slug = slugify(self.title)
            if not base_slug:  # Si slugify retourne une chaîne vide (caractères arabes, etc.)
                base_slug = f"article-{self.id or 'new'}"
            
            # Vérifier l'unicité du slug
            slug = base_slug
            counter = 1
            while RevueArticle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)


class Cart(TimeStampedModel):
    """Modèle pour le panier d'achat"""
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Utilisateur")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"
    
    def __str__(self):
        return f"Panier de {self.user.username}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Calcule le prix total du panier avec validation"""
        try:
            return sum(item.total_price for item in self.items.all() if item.total_price is not None)
        except (TypeError, ValueError):
            return 0


class CartItem(TimeStampedModel):
    """Modèle pour les éléments du panier"""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Panier")
    revue = models.ForeignKey(Revue, on_delete=models.CASCADE, verbose_name="Revue")
    format = models.CharField(max_length=10, choices=[('papier', 'Papier'), ('pdf', 'PDF')], verbose_name="Format")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    
    class Meta:
        verbose_name = "Élément du panier"
        verbose_name_plural = "Éléments du panier"
        unique_together = ['cart', 'revue', 'format']
    
    def __str__(self):
        return f"{self.revue} ({self.format}) x{self.quantity}"
    
    def clean(self):
        """Validation des données avant sauvegarde"""
        from django.core.exceptions import ValidationError
        
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError("La quantité doit être supérieure à 0")
        
        if self.revue is None:
            raise ValidationError("Une revue doit être sélectionnée")
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation"""
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def total_price(self):
        """Calcule le prix total avec validation des valeurs"""
        try:
            if self.format == 'papier':
                price = self.revue.price_paper
            else:
                price = self.revue.price_pdf
            
            if price is None or self.quantity is None:
                return 0
            return price * self.quantity
        except (TypeError, ValueError, AttributeError):
            return 0


class Order(TimeStampedModel):
    """Modèle pour les commandes"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('processing', 'En traitement'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Utilisateur")
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de commande")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    
    # Adresse de livraison
    shipping_address = models.TextField(verbose_name="Adresse de livraison")
    shipping_city = models.CharField(max_length=100, verbose_name="Ville")
    shipping_country = CountryField(verbose_name="Pays")
    shipping_postal_code = models.CharField(max_length=20, verbose_name="Code postal")
    
    # Paiement
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais de livraison")
    payment_method = models.CharField(max_length=50, verbose_name="Méthode de paiement")
    
    # Suivi
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Numéro de suivi")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commande {self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"CMD{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class OrderItem(TimeStampedModel):
    """Modèle pour les éléments de commande"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Commande")
    revue = models.ForeignKey(Revue, on_delete=models.CASCADE, verbose_name="Revue")
    format = models.CharField(max_length=10, choices=[('papier', 'Papier'), ('pdf', 'PDF')], verbose_name="Format")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    
    class Meta:
        verbose_name = "Élément de commande"
        verbose_name_plural = "Éléments de commande"
    
    def __str__(self):
        return f"{self.revue} ({self.format}) x{self.quantity}"
    
    def clean(self):
        """Validation des données avant sauvegarde"""
        from django.core.exceptions import ValidationError
        
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError("La quantité doit être supérieure à 0")
        
        if self.revue is None:
            raise ValidationError("Une revue doit être sélectionnée")
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation"""
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def total_price(self):
        """Calcule le prix total avec validation des valeurs"""
        if self.unit_price is None or self.quantity is None:
            return 0
        try:
            return self.unit_price * self.quantity
        except (TypeError, ValueError):
            return 0
