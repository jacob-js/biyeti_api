# Generated by Django 3.2.9 on 2022-07-11 11:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_category_cover'),
        ('tickets', '0012_purchase_payment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0005_payment_paid'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('user', 'event', 'ticket', 'paid')},
        ),
    ]