# Generated by Django 3.2.9 on 2021-11-11 13:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0004_purchase_available'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='purchase',
            unique_together={('ticket', 'user', 'interval', 'available')},
        ),
    ]