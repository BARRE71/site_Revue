from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

def login_view(request):
    """Vue de connexion fonctionnelle"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.username} ! Connexion réussie.')
                return redirect('core:home')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    context = {
        'site_name': 'RevueMaroc',
    }
    return render(request, 'users/login.html', context)


def register_view(request):
    """Vue d'inscription fonctionnelle"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        terms = request.POST.get('terms')
        newsletter = request.POST.get('newsletter')
        
        # Validation des champs
        if not all([username, email, password1, password2, first_name, last_name, terms]):
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
        elif password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
        elif len(password1) < 8:
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur est déjà pris.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Cette adresse email est déjà utilisée.')
        else:
            try:
                # Créer l'utilisateur
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Inscrire à la newsletter si demandé
                if newsletter:
                    from subscriptions.models import NewsletterSubscription
                    NewsletterSubscription.objects.create(
                        email=email,
                        is_active=True
                    )
                
                # Connecter automatiquement l'utilisateur
                login(request, user)
                messages.success(request, f'Compte créé avec succès ! Bienvenue {username} !')
                return redirect('core:home')
                
            except Exception as e:
                messages.error(request, f'Erreur lors de la création du compte : {str(e)}')
    
    context = {
        'site_name': 'RevueMaroc',
    }
    return render(request, 'users/register.html', context)


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """Vue de profil utilisateur avec statistiques"""
    from livres.models import Order, RevueArticle
    
    # Statistiques utilisateur
    user_orders = Order.objects.filter(user=request.user).count()
    user_articles = RevueArticle.objects.filter(revue__status='published').count()  # Articles disponibles
    user_subscriptions = 0  # À implémenter avec le système d'abonnements
    
    context = {
        'site_name': 'RevueMaroc',
        'user_orders': user_orders,
        'user_articles': user_articles,
        'user_subscriptions': user_subscriptions,
    }
    return render(request, 'users/profile.html', context)


@login_required
def change_password_view(request):
    """Vue pour changer le mot de passe"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Validation des champs
        if not all([old_password, new_password1, new_password2]):
            messages.error(request, 'Veuillez remplir tous les champs.')
        elif new_password1 != new_password2:
            messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
        elif len(new_password1) < 8:
            messages.error(request, 'Le nouveau mot de passe doit contenir au moins 8 caractères.')
        else:
            # Vérifier l'ancien mot de passe
            if request.user.check_password(old_password):
                try:
                    # Changer le mot de passe
                    request.user.set_password(new_password1)
                    request.user.save()
                    
                    # Reconnecter l'utilisateur (car set_password déconnecte)
                    from django.contrib.auth import update_session_auth_hash
                    update_session_auth_hash(request, request.user)
                    
                    messages.success(request, 'Votre mot de passe a été changé avec succès !')
                    return redirect('users:profile')
                except Exception as e:
                    messages.error(request, f'Erreur lors du changement de mot de passe : {str(e)}')
            else:
                messages.error(request, 'L\'ancien mot de passe est incorrect.')
    
    return redirect('users:profile')


@login_required
def edit_profile_view(request):
    """Vue pour éditer le profil utilisateur"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Validation des champs
        if not all([first_name, last_name, email]):
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
        elif len(first_name) < 2:
            messages.error(request, 'Le prénom doit contenir au moins 2 caractères.')
        elif len(last_name) < 2:
            messages.error(request, 'Le nom doit contenir au moins 2 caractères.')
        else:
            try:
                # Vérifier si l'email est déjà utilisé par un autre utilisateur
                if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                    messages.error(request, 'Cette adresse email est déjà utilisée par un autre compte.')
                else:
                    # Mettre à jour le profil
                    request.user.first_name = first_name
                    request.user.last_name = last_name
                    request.user.email = email
                    request.user.save()
                    
                    messages.success(request, 'Votre profil a été mis à jour avec succès !')
                    return redirect('users:profile')
                    
            except Exception as e:
                messages.error(request, f'Erreur lors de la mise à jour du profil : {str(e)}')
    
    return redirect('users:profile')
