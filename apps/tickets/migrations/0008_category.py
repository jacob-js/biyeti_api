# Generated by Django 3.2.9 on 2022-03-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_auto_20220306_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
