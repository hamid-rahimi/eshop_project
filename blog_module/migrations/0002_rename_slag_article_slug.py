# Generated by Django 4.2 on 2024-04-09 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_module', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='slag',
            new_name='slug',
        ),
    ]
