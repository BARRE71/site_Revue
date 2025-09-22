from django.contrib.auth.models import User
from .models import Subscription, NewsletterSubscription


def has_active_subscription(user):
    """
    Vérifie si un utilisateur a un abonnement actif
    """
    if not user or not user.is_authenticated:
        return False
    
    active_subscription = Subscription.objects.filter(
        user=user,
        status='active'
    ).first()
    
    return active_subscription and active_subscription.is_active


def get_user_subscription(user):
    """
    Récupère l'abonnement actif d'un utilisateur
    """
    if not user or not user.is_authenticated:
        return None
    
    return Subscription.objects.filter(
        user=user,
        status='active'
    ).first()


def is_newsletter_subscriber(user):
    """
    Vérifie si un utilisateur est abonné à la newsletter
    """
    if not user or not user.is_authenticated:
        return False
    
    return NewsletterSubscription.objects.filter(
        email=user.email,
        is_active=True
    ).exists()


def get_subscription_benefits(user):
    """
    Retourne les avantages disponibles pour un utilisateur
    """
    benefits = {
        'can_download_pdf': False,
        'can_access_full_content': False,
        'has_newsletter': False,
        'has_discounts': False,
        'has_priority_support': False,
    }
    
    if not user or not user.is_authenticated:
        return benefits
    
    # Vérifier l'abonnement actif
    subscription = get_user_subscription(user)
    if subscription and subscription.is_active:
        benefits.update({
            'can_download_pdf': True,
            'can_access_full_content': True,
            'has_newsletter': True,
            'has_discounts': True,
            'has_priority_support': True,
        })
    
    # Vérifier l'abonnement newsletter (même sans abonnement payant)
    if is_newsletter_subscriber(user):
        benefits['has_newsletter'] = True
    
    return benefits


def get_subscription_context(user):
    """
    Retourne le contexte d'abonnement pour les templates
    """
    return {
        'has_active_subscription': has_active_subscription(user),
        'user_subscription': get_user_subscription(user),
        'is_newsletter_subscriber': is_newsletter_subscriber(user),
        'subscription_benefits': get_subscription_benefits(user),
    }
