from django.contrib import admin
from .models import Contact, Newsletter, SiteSettings, Category, Tag


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'country', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Informations de contact', {
            'fields': ('name', 'email', 'phone', 'country', 'city', 'address')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Statut', {
            'fields': ('is_read', 'response')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_sent', 'sent_at', 'subscribers_count', 'created_at']
    list_filter = ['is_sent', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'subscribers_count']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'content')
        }),
        ('Statut', {
            'fields': ('is_sent', 'sent_at')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'subscribers_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'monthly_price', 'yearly_price']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('site_name', 'site_description', 'logo', 'favicon')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('Réseaux sociaux', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Configuration des abonnements', {
            'fields': ('monthly_price', 'yearly_price')
        }),
        ('Configuration des livres', {
            'fields': ('shipping_cost', 'free_shipping_threshold')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Permettre seulement une instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'order']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Affichage', {
            'fields': ('is_active', 'order')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'slug', 'color')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
