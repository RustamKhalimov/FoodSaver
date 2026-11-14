from django.conf import settings
from django.db import migrations


def create_existing_profiles(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    UserProfile = apps.get_model('accounts', 'UserProfile')
    database = schema_editor.connection.alias

    for user in User.objects.using(database).all().iterator():
        role = 'admin' if user.is_staff or user.is_superuser else 'customer'
        profile, created = UserProfile.objects.using(database).get_or_create(
            user_id=user.pk,
            defaults={'role': role},
        )
        if not created and role == 'admin' and profile.role != role:
            profile.role = role
            profile.save(using=database, update_fields=['role'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_existing_profiles, migrations.RunPython.noop),
    ]
