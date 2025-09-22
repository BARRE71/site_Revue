from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from core.models import TimeStampedModel, Category, Tag


class ArticleCategory(Category):
    """Catégorie spécifique aux articles (proxy model)"""
    
    class Meta:
        proxy = True
        verbose_name = "Catégorie d'article"
        verbose_name_plural = "Catégories d'articles"


class Article(TimeStampedModel):
    """Modèle pour les articles/blog"""
    
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'En attente'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="Extrait")
    content = models.TextField(verbose_name="Contenu")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, verbose_name="Catégorie")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    is_featured = models.BooleanField(default=False, verbose_name="Article en vedette")
    is_premium = models.BooleanField(default=False, verbose_name="Article premium")
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Image de couverture")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(TimeStampedModel):
    """Modèle pour les commentaires sur les articles"""
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="Article")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    content = models.TextField(verbose_name="Contenu")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.article.title}"
