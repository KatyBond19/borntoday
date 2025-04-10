# Generated by Django 5.1.7 on 2025-04-01 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star', '0006_alter_star_birth_date_alter_star_categories_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='star',
            options={'ordering': ['-time_create'], 'verbose_name': 'Знаменитости', 'verbose_name_plural': 'Знаменитости'},
        ),
        migrations.AlterField(
            model_name='star',
            name='birth_date',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='star',
            name='categories',
            field=models.ManyToManyField(related_name='stars', to='star.category', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='star',
            name='content',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='star',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='star.country', verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='star',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='star',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='star',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Время изменения'),
        ),
    ]
