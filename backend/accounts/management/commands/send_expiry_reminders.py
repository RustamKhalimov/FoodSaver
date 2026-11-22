from datetime import time, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.utils import timezone

from accounts.models import ReminderDelivery, UserProfile
from products.models import Product


def parse_time(value):
    try:
        return time.fromisoformat(value)
    except ValueError as error:
        raise CommandError('Time must use HH:MM format.') from error


class Command(BaseCommand):
    help = 'Send each enabled customer a daily email about products expiring soon.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--at',
            type=parse_time,
            help='Target reminder time in local project time (HH:MM); defaults to now.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List matching reminders without sending or recording them.',
        )

    def handle(self, *args, **options):
        now = timezone.localtime()
        target_time = options['at'] or now.time().replace(second=0, microsecond=0)
        today = timezone.localdate(now)
        last_expiry_day = today + timedelta(days=3)
        expiring_products = list(
            Product.objects.filter(
                quantity__gt=0,
                expiry_date__gte=today,
                expiry_date__lte=last_expiry_day,
            ).order_by('expiry_date', 'name')
        )

        if not expiring_products:
            self.stdout.write('No in-stock products expire within three days.')
            return

        recipients = UserProfile.objects.select_related('user').filter(
            notifications_enabled=True,
            reminder_time=target_time,
        ).order_by('user_id')

        sent = 0
        skipped = 0
        errors = 0
        for profile in recipients:
            user = profile.user
            email = user.email.strip()
            if not email:
                self.stderr.write(f'Skipped {user.username}: account has no email.')
                skipped += 1
                continue

            if options['dry_run']:
                self.stdout.write(
                    f'Would email {email} with {len(expiring_products)} expiring products.'
                )
                continue

            try:
                delivery, created = ReminderDelivery.objects.get_or_create(
                    user=user,
                    delivery_date=today,
                    defaults={'products_count': len(expiring_products)},
                )
            except IntegrityError:
                created = False
                delivery = None

            if not created:
                skipped += 1
                continue

            lines = [
                f"- {product.name}: expires {product.expiry_date.isoformat()} "
                f"({product.quantity} available)"
                for product in expiring_products
            ]
            message = '\n'.join([
                f"Hello {user.first_name or user.username},",
                '',
                'These FoodSaver products expire within the next three days:',
                *lines,
                '',
                'Review your inventory in FoodSaver to plan before they expire.',
            ])

            try:
                delivered = send_mail(
                    subject='FoodSaver: products expiring soon',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as error:
                if delivery is not None:
                    delivery.delete()
                self.stderr.write(f'Email failed for {email}: {error}')
                errors += 1
                continue

            if delivered:
                sent += 1
            else:
                if delivery is not None:
                    delivery.delete()
                errors += 1

        self.stdout.write(
            f'Reminder run complete: sent={sent}, skipped={skipped}, errors={errors}.'
        )
        if errors:
            raise CommandError(f'{errors} reminder email(s) failed.')
