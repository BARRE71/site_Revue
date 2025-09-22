from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from .models import SubscriptionPlan, Subscription, NewsletterSubscription
from .utils import get_subscription_context


def plan_list(request):
    """Vue pour afficher les plans d'abonnement"""
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    
    # Contexte d'abonnement
    subscription_context = get_subscription_context(request.user)
    
    context = {
        'plans': plans,
        **subscription_context,
    }
    
    return render(request, 'subscriptions/plan_list.html', context)


def subscribe(request, plan_id):
    """Vue pour s'abonner à un plan"""
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    
    if not request.user.is_authenticated:
        messages.warning(request, 'Vous devez être connecté pour vous abonner.')
        return redirect('users:login')
    
    # Vérifier si l'utilisateur a déjà un abonnement actif
    existing_subscription = Subscription.objects.filter(
        user=request.user,
        status='active'
    ).first()
    
    if existing_subscription and existing_subscription.is_active:
        messages.info(request, 'Vous avez déjà un abonnement actif.')
        return redirect('subscriptions:my_subscription')
    
    # Ici vous pourriez intégrer Stripe ou un autre système de paiement
    # Pour l'instant, on simule la création d'un abonnement
    
    context = {
        'plan': plan,
        'user': request.user,
    }
    
    return render(request, 'subscriptions/subscribe.html', context)


@login_required
def my_subscription(request):
    """Vue pour afficher l'abonnement de l'utilisateur"""
    subscription = Subscription.objects.filter(
        user=request.user,
        status='active'
    ).first()
    
    context = {
        'subscription': subscription,
        'has_active_subscription': subscription and subscription.is_active,
    }
    
    return render(request, 'subscriptions/my_subscription.html', context)


@login_required
def cancel_subscription(request):
    """Vue pour annuler un abonnement"""
    subscription = Subscription.objects.filter(
        user=request.user,
        status='active'
    ).first()
    
    if not subscription:
        messages.warning(request, 'Vous n\'avez pas d\'abonnement actif.')
        return redirect('subscriptions:plan_list')
    
    if request.method == 'POST':
        subscription.status = 'cancelled'
        subscription.save()
        messages.success(request, 'Votre abonnement a été annulé.')
        return redirect('subscriptions:my_subscription')
    
    context = {
        'subscription': subscription,
    }
    
    return render(request, 'subscriptions/cancel_subscription.html', context)


@login_required
def subscription_history(request):
    """Vue pour afficher l'historique des abonnements"""
    subscriptions = Subscription.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    context = {
        'subscriptions': subscriptions,
    }
    
    return render(request, 'subscriptions/subscription_history.html', context)


def newsletter_unsubscribe(request, subscription_id):
    """Vue pour se désabonner de la newsletter"""
    newsletter_sub = get_object_or_404(NewsletterSubscription, id=subscription_id)
    
    if request.method == 'POST':
        newsletter_sub.is_active = False
        newsletter_sub.save()
        messages.success(request, 'Vous avez été désabonné de la newsletter.')
        return redirect('core:home')
    
    context = {
        'newsletter_subscription': newsletter_sub,
    }
    
    return render(request, 'subscriptions/newsletter_unsubscribe.html', context)