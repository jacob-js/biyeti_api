# Generated by Django 3.2.9 on 2022-07-11 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_alter_payment_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set(),
        ),
    ]
