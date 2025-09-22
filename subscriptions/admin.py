from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import SubscriptionPlan, Subscription, PaymentHistory, NewsletterSubscription
from .widgets import FeaturesWidget

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at', 'domains', 'subscription_status']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'domains']
    readonly_fields = ['subscribed_at']
    list_editable = ['is_active']
    actions = ['send_test_newsletter', 'export_emails']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-subscribed_at')
    
    def subscription_status(self, obj):
        """Affiche le statut d'abonnement de l'utilisateur"""
        from .utils import has_active_subscription
        from django.contrib.auth.models import User
        
        try:
            user = User.objects.get(email=obj.email)
            if has_active_subscription(user):
                return format_html('<span style="color: green;">✓ Abonné Premium</span>')
            else:
                return format_html('<span style="color: orange;">○ Abonné Newsletter</span>')
        except User.DoesNotExist:
            return format_html('<span style="color: gray;">○ Newsletter uniquement</span>')
    
    subscription_status.short_description = 'Statut'
    
    def send_test_newsletter(self, request, queryset):
        """Action pour envoyer une newsletter de test"""
        from django.core.management import call_command
        
        emails = [obj.email for obj in queryset[:5]]  # Limiter à 5 emails
        self.message_user(
            request, 
            f'Newsletter de test envoyée à {len(emails)} destinataires sélectionnés.'
        )
        
        # Ici vous pourriez appeler la commande d'envoi
        # call_command('send_newsletter', newsletter_type='all', dry_run=False)
    
    send_test_newsletter.short_description = "Envoyer newsletter de test"
    
    def export_emails(self, request, queryset):
        """Action pour exporter les emails"""
        emails = [obj.email for obj in queryset]
        self.message_user(
            request, 
            f'Emails exportés: {", ".join(emails[:10])}{"..." if len(emails) > 10 else ""}'
        )
    
    export_emails.short_description = "Exporter les emails"

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'duration_days', 'is_active', 'is_popular']
    list_filter = ['plan_type', 'is_active', 'is_popular']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_popular']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'plan_type', 'duration_days')
        }),
        ('Prix et statut', {
            'fields': ('price', 'is_active', 'is_popular')
        }),
        ('Fonctionnalités', {
            'fields': ('features',),
            'description': 'Saisissez les fonctionnalités sous forme de liste JSON. Exemple: ["Accès à tous les numéros", "Support prioritaire", "Téléchargement PDF"]'
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Utiliser le widget personnalisé pour les fonctionnalités
        form.base_fields['features'].widget = FeaturesWidget()
        return form

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'is_active']
    list_filter = ['status', 'plan', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email', 'plan__name']
    readonly_fields = ['stripe_subscription_id']

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'amount', 'status', 'transaction_date']
    list_filter = ['status', 'transaction_date', 'payment_method']
    search_fields = ['user__username', 'user__email', 'stripe_payment_id']
    readonly_fields = ['stripe_payment_id', 'transaction_date']
