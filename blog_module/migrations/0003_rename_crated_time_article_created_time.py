# Generated by Django 4.2 on 2024-04-09 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_module', '0002_rename_slag_article_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='crated_time',
            new_name='created_time',
        ),
    ]
