# Generated by Django 5.1.7 on 2025-04-01 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star', '0003_category_slug_country_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='country',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
