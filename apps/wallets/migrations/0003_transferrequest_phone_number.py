# Generated by Django 3.2.9 on 2022-07-20 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0002_transferrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferrequest',
            name='phone_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
