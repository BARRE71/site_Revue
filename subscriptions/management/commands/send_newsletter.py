from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from subscriptions.models import NewsletterSubscription, Subscription
from livres.models import Revue
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Envoie une newsletter aux abonnés'

    def add_arguments(self, parser):
        parser.add_argument(
            '--newsletter-type',
            type=str,
            choices=['all', 'subscribers', 'premium'],
            default='all',
            help='Type de newsletter à envoyer'
        )
        parser.add_argument(
            '--subject',
            type=str,
            help='Sujet de la newsletter'
        )
        parser.add_argument(
            '--template',
            type=str,
            default='newsletter/default.html',
            help='Template à utiliser pour la newsletter'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulation sans envoi réel'
        )

    def handle(self, *args, **options):
        newsletter_type = options['newsletter_type']
        subject = options['subject'] or 'Newsletter RevueMaroc'
        template = options['template']
        dry_run = options['dry_run']

        self.stdout.write(f'Préparation de l\'envoi de newsletter: {newsletter_type}')

        # Récupérer les destinataires selon le type
        if newsletter_type == 'all':
            recipients = NewsletterSubscription.objects.filter(is_active=True)
        elif newsletter_type == 'subscribers':
            recipients = NewsletterSubscription.objects.filter(is_active=True)
        elif newsletter_type == 'premium':
            # Abonnés premium (avec abonnement payant)
            premium_users = Subscription.objects.filter(
                status='active'
            ).values_list('user__email', flat=True)
            recipients = NewsletterSubscription.objects.filter(
                email__in=premium_users,
                is_active=True
            )

        self.stdout.write(f'Nombre de destinataires: {recipients.count()}')

        if dry_run:
            self.stdout.write('Mode simulation - aucun email ne sera envoyé')
            for recipient in recipients[:5]:  # Afficher seulement les 5 premiers
                self.stdout.write(f'  - {recipient.email}')
            return

        # Récupérer les données pour la newsletter
        recent_revues = Revue.objects.filter(
            status='published'
        ).order_by('-publication_date')[:3]

        # Préparer le contexte
        context = {
            'recent_revues': recent_revues,
            'newsletter_type': newsletter_type,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }

        # Rendre le template
        try:
            html_content = render_to_string(template, context)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors du rendu du template: {e}')
            )
            return

        # Envoyer les emails
        success_count = 0
        error_count = 0

        for recipient in recipients:
            try:
                # Personnaliser le contexte pour chaque destinataire
                recipient_context = context.copy()
                recipient_context['recipient'] = recipient
                recipient_context['unsubscribe_url'] = f"{context['site_url']}/newsletter/unsubscribe/{recipient.id}/"

                # Rendre le contenu personnalisé
                personalized_html = render_to_string(template, recipient_context)

                # Créer l'email
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='Veuillez activer HTML pour voir cette newsletter.',
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@revuemaroc.com'),
                    to=[recipient.email]
                )
                msg.attach_alternative(personalized_html, "text/html")
                
                # Envoyer
                msg.send()
                success_count += 1
                
                if success_count % 10 == 0:
                    self.stdout.write(f'Envoyé: {success_count} emails')

            except Exception as e:
                error_count += 1
                logger.error(f'Erreur envoi newsletter à {recipient.email}: {e}')
                self.stdout.write(
                    self.style.ERROR(f'Erreur pour {recipient.email}: {e}')
                )

        # Résumé
        self.stdout.write(
            self.style.SUCCESS(
                f'Newsletter envoyée: {success_count} succès, {error_count} erreurs'
            )
        )
