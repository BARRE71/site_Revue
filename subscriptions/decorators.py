from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import Subscription


def subscription_required(view_func):
    """
    Décorateur pour vérifier qu'un utilisateur a un abonnement actif
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour accéder à cette fonctionnalité.')
            return redirect('users:login')
        
        # Vérifier si l'utilisateur a un abonnement actif
        active_subscription = Subscription.objects.filter(
            user=request.user,
            status='active'
        ).first()
        
        if not active_subscription or not active_subscription.is_active:
            messages.info(request, 'Un abonnement actif est requis pour accéder à cette fonctionnalité.')
            return redirect('subscriptions:plan_list')
        
        # Ajouter l'abonnement au contexte
        request.active_subscription = active_subscription
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def subscription_optional(view_func):
    """
    Décorateur pour vérifier l'abonnement mais permettre l'accès avec limitations
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            active_subscription = Subscription.objects.filter(
                user=request.user,
                status='active'
            ).first()
            request.has_active_subscription = active_subscription and active_subscription.is_active
        else:
            request.has_active_subscription = False
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
