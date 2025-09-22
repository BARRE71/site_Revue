from django.conf import settings
from .models import SiteSettings, Category, Tag


def global_context(request):
    """Contexte global disponible dans tous les templates"""
    context = {}
    
    try:
        # Paramètres du site
        site_settings = SiteSettings.objects.first()
        if site_settings:
            context['site_settings'] = site_settings
            context['site_name'] = site_settings.site_name
            context['site_description'] = site_settings.site_description
            context['contact_email'] = site_settings.contact_email
            context['contact_phone'] = site_settings.contact_phone
            context['monthly_price'] = site_settings.monthly_price
            context['yearly_price'] = site_settings.yearly_price
            context['shipping_cost'] = site_settings.shipping_cost
            context['free_shipping_threshold'] = site_settings.free_shipping_threshold
        else:
            # Valeurs par défaut si aucun paramètre n'est configuré
            context['site_name'] = 'RevueMaroc'
            context['site_description'] = 'Votre source d\'information sur le développement du Maroc'
            context['monthly_price'] = 9.99
            context['yearly_price'] = 99.99
            context['shipping_cost'] = 5.99
            context['free_shipping_threshold'] = 50.00
        
        # Catégories principales
        categories = Category.objects.filter(is_active=True).order_by('order', 'name')
        context['main_categories'] = categories[:8]  # Limiter à 8 catégories principales
        
        # Tags populaires
        tags = Tag.objects.all().order_by('name')[:20]  # Limiter à 20 tags
        context['popular_tags'] = tags
        
    except Exception as e:
        # En cas d'erreur, utiliser des valeurs par défaut
        context['site_name'] = 'RevueMaroc'
        context['main_categories'] = []
        context['popular_tags'] = []
    
    return context
