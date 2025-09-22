from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contact, SiteSettings, Category, Tag
from subscriptions.models import NewsletterSubscription


def home(request):
    """Page d'accueil avec revues en vedette et actualités importantes"""
    from livres.models import Revue, RevueArticle, Author, RevueCategory
    
    # Récupérer les revues en vedette
    featured_revues = Revue.objects.filter(
        is_featured=True, 
        status='published'
    ).order_by('-numero')[:3]
    
    # Récupérer la revue principale (la plus récente ou en vedette)
    main_revue = Revue.objects.filter(
        status='published'
    ).order_by('-publication_date', '-numero').first()
    
    # Récupérer les revues secondaires (4 autres)
    secondary_revues = Revue.objects.filter(
        status='published'
    ).exclude(id=main_revue.id if main_revue else None).order_by('-publication_date', '-numero')[:4]
    
    # Récupérer les articles récents
    recent_articles = RevueArticle.objects.filter(
        revue__status='published'
    ).select_related('revue', 'author').order_by('-revue__publication_date')[:6]
    
    # Récupérer les catégories principales
    main_categories = RevueCategory.objects.filter(is_active=True)[:6]
    
    # Statistiques
    total_revues = Revue.objects.filter(status='published').count()
    total_articles = RevueArticle.objects.count()
    total_authors = Author.objects.count()
    
    context = {
        'site_name': 'RevueMaroc',
        'site_description': 'Revue culturelle et littéraire du Maroc',
        'main_revue': main_revue,
        'featured_revues': featured_revues,
        'secondary_revues': secondary_revues,
        'recent_articles': recent_articles,
        'main_categories': main_categories,
        'stats': {
            'total_revues': total_revues,
            'total_articles': total_articles,
            'total_authors': total_authors,
        }
    }
    return render(request, 'core/home.html', context)


def about(request):
    """Page À propos temporaire"""
    context = {
        'site_name': 'RevueMaroc',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Page de contact avec sauvegarde en base et envoi d'email"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        phone = request.POST.get('phone', '').strip()
        country = request.POST.get('country', '').strip()
        city = request.POST.get('city', '').strip()
        address = request.POST.get('address', '').strip()
        
        # Validation des champs obligatoires
        if not all([name, email, subject, message]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        else:
            try:
                # Créer et sauvegarder le message de contact
                contact_message = Contact.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                    phone=phone if phone else '',
                    country=country if country else '',
                    city=city if city else '',
                    address=address if address else ''
                )
                
                # Envoyer un email de confirmation (simulé pour l'instant)
                # TODO: Intégrer un vrai service d'email comme SendGrid ou Mailgun
                print(f"Email de confirmation envoyé à {email} pour le message: {subject}")
                
                messages.success(request, f"Votre message '{subject}' a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.")
                return redirect('core:home')
                
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'envoi du message: {str(e)}")
    
    context = {
        'site_name': 'RevueMaroc',
    }
    return render(request, 'core/contact.html', context)


def search(request):
    """Page de recherche temporaire"""
    context = {
        'site_name': 'RevueMaroc',
    }
    return render(request, 'core/search.html', context)


@login_required
def dashboard(request):
    """Tableau de bord utilisateur avec statistiques"""
    from livres.models import Revue, RevueArticle, Author, Cart
    
    # Statistiques générales
    total_revues = Revue.objects.filter(status='published').count()
    total_articles = RevueArticle.objects.count()
    total_authors = Author.objects.count()
    
    # Statistiques utilisateur
    try:
        user_cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items = user_cart.items.count()
    except Cart.DoesNotExist:
        cart_items = 0
    
    # Revues récentes
    recent_revues = Revue.objects.filter(status='published').order_by('-publication_date')[:3]
    
    context = {
        'site_name': 'RevueMaroc',
        'stats': {
            'total_revues': total_revues,
            'total_articles': total_articles,
            'total_authors': total_authors,
            'cart_items': cart_items,
        },
        'recent_revues': recent_revues,
    }
    return render(request, 'core/dashboard.html', context)


def newsletter_subscribe(request):
    """Inscription newsletter avec sauvegarde en base et gestion des doublons"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, "Veuillez saisir une adresse email valide.")
        else:
            try:
                # Vérifier si l'email existe déjà
                existing_subscription = NewsletterSubscription.objects.filter(email=email).first()
                
                if existing_subscription:
                    if existing_subscription.is_active:
                        messages.info(request, "Cette adresse email est déjà inscrite à notre newsletter.")
                    else:
                        # Réactiver l'abonnement
                        existing_subscription.is_active = True
                        existing_subscription.save()
                        messages.success(request, "Votre abonnement à la newsletter a été réactivé avec succès!")
                else:
                    # Créer un nouvel abonnement
                    NewsletterSubscription.objects.create(
                        email=email,
                        is_active=True
                    )
                    messages.success(request, "Inscription à la newsletter réussie! Vous recevrez nos dernières actualités.")
                
                # Envoyer un email de confirmation (simulé pour l'instant)
                # TODO: Intégrer un vrai service d'email
                print(f"Email de confirmation newsletter envoyé à {email}")
                
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'inscription: {str(e)}")
    
    return redirect('core:home')


def newsletter_unsubscribe(request):
    """Désinscription de la newsletter"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, "Veuillez saisir une adresse email valide.")
        else:
            try:
                # Vérifier si l'email existe
                subscription = NewsletterSubscription.objects.filter(email=email).first()
                
                if subscription:
                    if subscription.is_active:
                        subscription.is_active = False
                        subscription.save()
                        messages.success(request, "Vous avez été désinscrit de notre newsletter avec succès.")
                    else:
                        messages.info(request, "Cette adresse email n'était pas inscrite à notre newsletter.")
                else:
                    messages.info(request, "Cette adresse email n'était pas inscrite à notre newsletter.")
                    
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de la désinscription: {str(e)}")
        
        return redirect('core:home')
    
    # Afficher le formulaire de désinscription
    context = {
        'site_name': 'RevueMaroc',
    }
    return render(request, 'core/newsletter_unsubscribe.html', context)


@login_required
def newsletter_subscribers(request):
    """Liste des abonnés à la newsletter (admin uniquement)"""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('core:home')
    
    subscribers = NewsletterSubscription.objects.all().order_by('-created_at')
    
    context = {
        'subscribers': subscribers,
        'total_subscribers': subscribers.count(),
        'active_subscribers': subscribers.filter(is_active=True).count(),
    }
    
    return render(request, 'core/newsletter_subscribers.html', context)


def sitemap(request):
    """Plan du site temporaire"""
    context = {
        'site_name': 'RevueMaroc',
    }
    return render(request, 'core/sitemap.html', context)


def category_detail(request, slug):
    """Détail de catégorie temporaire"""
    context = {
        'site_name': 'RevueMaroc',
        'category_name': slug,
    }
    return render(request, 'core/category_detail.html', context)
