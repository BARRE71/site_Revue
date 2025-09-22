from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Revue, RevueArticle, Author, RevueCategory,
    Cart, CartItem, Order, OrderItem
)


@admin.register(RevueCategory)
class RevueCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'academic_title', 'institution', 'country', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'country', 'created_at']
    search_fields = ['name', 'academic_title', 'institution']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'bio', 'photo')
        }),
        ('Informations académiques', {
            'fields': ('academic_title', 'institution', 'country')
        }),
        ('Web et marketing', {
            'fields': ('website', 'is_featured')
        }),
    )


class RevueArticleInline(admin.TabularInline):
    model = RevueArticle
    extra = 1
    fields = ['title', 'author', 'page_start', 'page_end', 'abstract']


@admin.register(Revue)
class RevueAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'title', 'language', 'format', 'status', 
        'price_paper', 'price_pdf', 'stock_paper', 'stock_pdf',
        'views_count', 'downloads_count', 'is_featured', 'publication_date'
    ]
    list_filter = [
        'status', 'format', 'language', 'is_featured', 
        'is_bestseller', 'publication_date', 'category'
    ]
    search_fields = ['numero', 'title', 'subtitle', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-numero']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('numero', 'title', 'subtitle', 'slug', 'category', 'tags')
        }),
        ('Contenu', {
            'fields': ('description', 'excerpt', 'editorial')
        }),
        ('Métadonnées', {
            'fields': ('language', 'pages_count', 'dimensions', 'isbn', 'issn')
        }),
        ('Publication', {
            'fields': ('publication_date', 'format', 'status')
        }),
        ('Prix et stock', {
            'fields': ('price_paper', 'price_pdf', 'stock_paper', 'stock_pdf')
        }),
        ('Marketing', {
            'fields': ('is_featured', 'is_bestseller', 'cover_image', 'pdf_file')
        }),
        ('Statistiques', {
            'fields': ('sales_count', 'rating', 'views_count', 'downloads_count'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [RevueArticleInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('tags')
    
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.cover_image.url
            )
        return "Aucune image"
    cover_preview.short_description = "Aperçu couverture"


@admin.register(RevueArticle)
class RevueArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'revue', 'author', 'page_start', 'page_end', 'created_at']
    list_filter = ['revue', 'author', 'created_at']
    search_fields = ['title', 'abstract', 'keywords']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['revue', 'page_start']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'revue', 'author')
        }),
        ('Contenu', {
            'fields': ('abstract', 'content', 'keywords')
        }),
        ('Pages', {
            'fields': ('page_start', 'page_end')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('revue', 'author')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']
    
    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = "Articles"
    
    def total_price(self, obj):
        return f"{obj.total_price:.2f} €"
    total_price.short_description = "Total"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'revue', 'format', 'quantity', 'total_price']
    list_filter = ['format', 'created_at']
    search_fields = ['cart__user__username', 'revue__title']
    ordering = ['-created_at']
    
    def total_price(self, obj):
        return f"{obj.total_price:.2f} €"
    total_price.short_description = "Total"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['revue', 'format', 'quantity', 'unit_price', 'total_price']
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'status', 'total_amount', 
        'shipping_cost', 'payment_method', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'shipping_country', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations de commande', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Adresse de livraison', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_country', 'shipping_postal_code')
        }),
        ('Paiement', {
            'fields': ('total_amount', 'shipping_cost', 'payment_method')
        }),
        ('Suivi', {
            'fields': ('tracking_number', 'notes')
        }),
    )
    
    inlines = [OrderItemInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def total_with_shipping(self, obj):
        total = obj.total_amount + obj.shipping_cost
        return f"{total:.2f} €"
    total_with_shipping.short_description = "Total + livraison"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'revue', 'format', 'quantity', 'unit_price', 'total_price']
    list_filter = ['format', 'created_at']
    search_fields = ['order__order_number', 'revue__title']
    ordering = ['-created_at']
    
    def total_price(self, obj):
        return f"{obj.total_price:.2f} €"
    total_price.short_description = "Total"


# Configuration de l'admin
admin.site.site_header = "Administration Revue Délibérée"
admin.site.site_title = "Revue Délibérée"
admin.site.index_title = "Gestion de la Revue Intellectuelle"
