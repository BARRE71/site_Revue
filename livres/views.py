from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Revue, RevueArticle, Author, RevueCategory, Cart, CartItem, Order, OrderItem
from .forms import RevueFilterForm
from subscriptions.decorators import subscription_required, subscription_optional
from subscriptions.utils import get_subscription_context


def revue_list(request):
    """Vue pour afficher le catalogue des revues avec filtres et tri"""
    
    # Récupération des paramètres de filtrage
    form = RevueFilterForm(request.GET)
    
    # Base queryset
    revues = Revue.objects.filter(status='published').select_related('category')
    
    # Application des filtres
    if form.is_valid():
        # Filtre par catégorie
        if form.cleaned_data.get('category'):
            revues = revues.filter(category=form.cleaned_data['category'])
        
        # Filtre par langue
        if form.cleaned_data.get('language'):
            revues = revues.filter(language=form.cleaned_data['language'])
        
        # Filtre par format
        if form.cleaned_data.get('format'):
            if form.cleaned_data['format'] == 'papier':
                revues = revues.filter(format__in=['papier', 'both'])
            elif form.cleaned_data['format'] == 'pdf':
                revues = revues.filter(format__in=['pdf', 'both'])
        
        # Filtre par prix
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        if min_price:
            revues = revues.filter(price_paper__gte=min_price)
        if max_price:
            revues = revues.filter(price_paper__lte=max_price)
        
        # Filtre par année
        year = form.cleaned_data.get('year')
        if year:
            revues = revues.filter(publication_date__year=year)
        
        # Filtre par thème (recherche dans titre et description)
        theme = form.cleaned_data.get('theme')
        if theme:
            revues = revues.filter(
                Q(title__icontains=theme) |
                Q(subtitle__icontains=theme) |
                Q(description__icontains=theme) |
                Q(tags__name__icontains=theme)
            ).distinct()
    
    # Tri
    sort_by = request.GET.get('sort', 'numero')
    if sort_by == 'prix_croissant':
        revues = revues.order_by('price_paper')
    elif sort_by == 'prix_decroissant':
        revues = revues.order_by('-price_paper')
    elif sort_by == 'nouveautes':
        revues = revues.order_by('-publication_date')
    elif sort_by == 'popularite':
        revues = revues.order_by('-sales_count')
    else:  # Par défaut : par numéro décroissant
        revues = revues.order_by('-numero')
    
    # Pagination
    paginator = Paginator(revues, 12)  # 12 revues par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Contexte
    context = {
        'page_obj': page_obj,
        'form': form,
        'categories': RevueCategory.objects.filter(is_active=True),
        'languages': Revue.LANGUAGE_CHOICES,
        'formats': Revue.FORMAT_CHOICES,
        'years': Revue.objects.filter(status='published').dates('publication_date', 'year'),
        'total_revues': revues.count(),
        'sort_options': [
            ('numero', 'Numéro'),
            ('nouveautes', 'Nouveautés'),
            ('prix_croissant', 'Prix croissant'),
            ('prix_decroissant', 'Prix décroissant'),
            ('popularite', 'Popularité'),
        ]
    }
    
    return render(request, 'livres/revue_list.html', context)


@subscription_optional
def revue_detail(request, slug):
    """Vue pour afficher le détail d'une revue"""
    
    revue = get_object_or_404(
        Revue.objects.select_related('category').prefetch_related('tags', 'articles__author'),
        slug=slug,
        status='published'
    )
    
    # Incrémenter le compteur de vues
    revue.views_count += 1
    revue.save(update_fields=['views_count'])
    
    # Récupérer les articles de la revue
    articles = revue.articles.all().select_related('author').order_by('page_start')
    
    # Revues similaires (même catégorie ou tags)
    similar_revues = Revue.objects.filter(
        status='published'
    ).exclude(id=revue.id).filter(
        Q(category=revue.category) | Q(tags__in=revue.tags.all())
    ).distinct()[:4]
    
    # Revues récentes
    recent_revues = Revue.objects.filter(
        status='published'
    ).exclude(id=revue.id).order_by('-publication_date')[:4]
    
    # Contexte d'abonnement
    subscription_context = get_subscription_context(request.user)
    
    context = {
        'revue': revue,
        'articles': articles,
        'similar_revues': similar_revues,
        'recent_revues': recent_revues,
        **subscription_context,
    }
    
    return render(request, 'livres/revue_detail.html', context)


@subscription_required
def download_revue_pdf(request, slug):
    """Vue pour télécharger le PDF d'une revue (réservée aux abonnés)"""
    
    revue = get_object_or_404(
        Revue.objects.select_related('category'),
        slug=slug,
        status='published'
    )
    
    if not revue.pdf_file:
        messages.error(request, 'Le fichier PDF de cette revue n\'est pas disponible.')
        return redirect('livres:revue_detail', slug=slug)
    
    # Vérifier que l'utilisateur a un abonnement actif
    if not request.active_subscription:
        messages.warning(request, 'Un abonnement actif est requis pour télécharger les PDF.')
        return redirect('subscriptions:plan_list')
    
    # Incrémenter le compteur de téléchargements
    revue.downloads_count += 1
    revue.save(update_fields=['downloads_count'])
    
    # Retourner le fichier PDF
    from django.http import FileResponse
    import os
    
    file_path = revue.pdf_file.path
    if os.path.exists(file_path):
        response = FileResponse(
            open(file_path, 'rb'),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{revue.title}.pdf"'
        return response
    else:
        messages.error(request, 'Le fichier PDF est introuvable.')
        return redirect('livres:revue_detail', slug=slug)


def author_detail(request, slug):
    """Vue pour afficher le détail d'un auteur"""
    
    author = get_object_or_404(Author, slug=slug)
    
    # Récupérer les articles de l'auteur
    articles = RevueArticle.objects.filter(author=author).select_related('revue').order_by('-revue__publication_date')
    
    # Récupérer les revues où l'auteur a publié
    revues = Revue.objects.filter(articles__author=author).distinct().order_by('-publication_date')
    
    context = {
        'author': author,
        'articles': articles,
        'revues': revues,
    }
    
    return render(request, 'livres/author_detail.html', context)


@login_required
def add_to_cart(request, revue_id):
    """Vue pour ajouter une revue au panier"""
    
    if request.method == 'POST':
        revue = get_object_or_404(Revue, id=revue_id, status='published')
        format_type = request.POST.get('format')
        quantity = int(request.POST.get('quantity', 1))
        
        # Validation du format
        if format_type == 'papier' and not revue.is_available_paper:
            messages.error(request, "Le format papier n'est pas disponible pour cette revue.")
            return redirect('livres:revue_detail', slug=revue.slug)
        
        if format_type == 'pdf' and not revue.is_available_pdf:
            messages.error(request, "Le format PDF n'est pas disponible pour cette revue.")
            return redirect('livres:revue_detail', slug=revue.slug)
        
        # Récupérer ou créer le panier de l'utilisateur
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        
        # Vérifier si l'article est déjà dans le panier
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            revue=revue,
            format=format_type,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"'{revue.title}' a été ajouté à votre panier.")
        return redirect('livres:cart_detail')
    
    return redirect('livres:revue_list')


@login_required
def cart_detail(request):
    """Vue pour afficher le détail du panier"""
    
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items = cart.items.all().select_related('revue')
        
        # Calculer les totaux
        cart_total = sum(item.total_price for item in cart_items)
        
        # Frais de livraison (à implémenter selon la logique métier)
        shipping_cost = 0
        total_with_shipping = cart_total + shipping_cost
        
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        cart_total = 0
        shipping_cost = 0
        total_with_shipping = 0
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_cost': shipping_cost,
        'total_with_shipping': total_with_shipping,
    }
    
    return render(request, 'livres/cart_detail.html', context)


def cart_count(request):
    """Vue pour obtenir le nombre d'articles dans le panier (AJAX)"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
            count = cart.items.count()
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0
    
    return JsonResponse({'count': count})


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Vue pour mettre à jour la quantité d'un article du panier"""
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Quantité mise à jour.")
        else:
            cart_item.delete()
            messages.success(request, "Article supprimé du panier.")
            
    except CartItem.DoesNotExist:
        messages.error(request, "Article non trouvé.")
    
    return redirect('livres:cart_detail')


@login_required
@require_POST
def remove_cart_item(request, item_id):
    """Vue pour supprimer un article du panier"""
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, "Article supprimé du panier.")
    except CartItem.DoesNotExist:
        messages.error(request, "Article non trouvé.")
    
    return redirect('livres:cart_detail')


def search_revues(request):
    """Vue pour la recherche de revues"""
    
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Recherche dans les revues
        revues = Revue.objects.filter(
            status='published'
        ).filter(
            Q(title__icontains=query) |
            Q(subtitle__icontains=query) |
            Q(description__icontains=query) |
            Q(editorial__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        
        # Recherche dans les articles
        articles = RevueArticle.objects.filter(
            Q(title__icontains=query) |
            Q(abstract__icontains=query) |
            Q(keywords__icontains=query)
        ).select_related('revue', 'author')
        
        # Recherche dans les auteurs
        authors = Author.objects.filter(
            Q(name__icontains=query) |
            Q(bio__icontains=query) |
            Q(academic_title__icontains=query) |
            Q(institution__icontains=query)
        )
        
        results = {
            'revues': revues,
            'articles': articles,
            'authors': authors,
            'query': query
        }
    
    context = {
        'results': results,
        'query': query,
    }
    
    return render(request, 'livres/search_results.html', context)


def category_revues(request, category_slug):
    """Vue pour afficher les revues d'une catégorie"""
    
    category = get_object_or_404(RevueCategory, slug=category_slug, is_active=True)
    revues = Revue.objects.filter(
        category=category,
        status='published'
    ).order_by('-numero')
    
    # Pagination
    paginator = Paginator(revues, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'total_revues': revues.count(),
    }
    
    return render(request, 'livres/category_revues.html', context)


@login_required
def checkout(request):
    """Vue pour le processus de commande (checkout)"""
    
    from decimal import Decimal
    
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items = cart.items.all().select_related('revue')
        
        if not cart_items.exists():
            messages.warning(request, "Votre panier est vide.")
            return redirect('livres:cart_detail')
        
        # Calculer les totaux
        cart_total = sum(item.total_price for item in cart_items)
        
        # Frais de livraison (logique simplifiée)
        shipping_cost = Decimal('0')
        if any(item.format == 'papier' for item in cart_items):
            shipping_cost = Decimal('5.00')  # Frais de livraison pour le papier
        
        total_with_shipping = cart_total + shipping_cost
        
        if request.method == 'POST':
            # Traitement du formulaire de commande
            shipping_address = request.POST.get('shipping_address')
            shipping_city = request.POST.get('shipping_city')
            shipping_country = request.POST.get('shipping_country')
            shipping_postal_code = request.POST.get('shipping_postal_code')
            payment_method = request.POST.get('payment_method')
            
            if all([shipping_address, shipping_city, shipping_country, shipping_postal_code, payment_method]):
                # Créer la commande
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=shipping_address,
                    shipping_city=shipping_city,
                    shipping_country=shipping_country,
                    shipping_postal_code=shipping_postal_code,
                    total_amount=total_with_shipping,
                    shipping_cost=shipping_cost,
                    payment_method=payment_method
                )
                
                # Créer les éléments de commande
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        revue=item.revue,
                        format=item.format,
                        quantity=item.quantity,
                        unit_price=item.revue.price_paper if item.format == 'papier' else item.revue.price_pdf
                    )
                
                # Vider le panier
                cart.is_active = False
                cart.save()
                
                messages.success(request, f"Votre commande {order.order_number} a été créée avec succès !")
                return redirect('livres:order_detail', order_id=order.id)
            else:
                messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        cart_total = 0
        shipping_cost = 0
        total_with_shipping = 0
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_cost': shipping_cost,
        'total_with_shipping': total_with_shipping,
    }
    
    return render(request, 'livres/checkout.html', context)


@login_required
def order_detail(request, order_id):
    """Vue pour afficher le détail d'une commande"""
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'livres/order_detail.html', context)


@login_required
def order_list(request):
    """Vue pour afficher la liste des commandes de l'utilisateur"""
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'livres/order_list.html', context)
