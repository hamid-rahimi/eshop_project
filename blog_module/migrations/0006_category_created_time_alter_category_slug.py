# Generated by Django 4.2 on 2024-04-13 01:18

from django.db import migrations, models
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog_module', '0005_category_slug_alter_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(allow_unicode=True, blank=True, editable=False, populate_from=['title', 'parent__title'], unique=True),
        ),
    ]
