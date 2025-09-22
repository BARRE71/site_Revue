from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from livres.models import RevueArticle, RevueCategory
from subscriptions.utils import get_subscription_context

def article_list(request):
    """Liste des articles de revue"""
    # Récupérer les articles de revue
    articles = RevueArticle.objects.select_related('revue', 'author', 'revue__category').order_by('-revue__publication_date')
    
    # Filtrage par recherche
    search_query = request.GET.get('q', '')
    if search_query:
        articles = articles.filter(title__icontains=search_query)
    
    # Filtrage par catégorie
    category_slug = request.GET.get('category', '')
    if category_slug:
        articles = articles.filter(revue__category__slug=category_slug)
    
    # Pagination
    paginator = Paginator(articles, 9)  # 9 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Récupérer les catégories pour le filtre
    categories = RevueCategory.objects.filter(is_active=True)
    
    # Contexte d'abonnement
    subscription_context = get_subscription_context(request.user)
    
    context = {
        'site_name': 'RevueMaroc',
        'articles': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        **subscription_context,
    }
    return render(request, 'articles/article_list.html', context)


def article_detail(request, slug):
    """Détail d'un article de revue"""
    article = get_object_or_404(RevueArticle, slug=slug)
    
    # Articles similaires (même catégorie)
    similar_articles = RevueArticle.objects.filter(
        revue__category=article.revue.category
    ).exclude(id=article.id).order_by('-revue__publication_date')[:3]
    
    # Traitement des mots-clés
    keywords_list = []
    if article.keywords:
        keywords_list = [keyword.strip() for keyword in article.keywords.split(',') if keyword.strip()]
    
    # Contexte d'abonnement
    subscription_context = get_subscription_context(request.user)
    
    context = {
        'site_name': 'RevueMaroc',
        'article': article,
        'similar_articles': similar_articles,
        'keywords_list': keywords_list,
        **subscription_context,
    }
    return render(request, 'articles/article_detail.html', context)
