# Generated by Django 4.2 on 2024-04-13 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_module', '0007_alter_article_slug_alter_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published'), ('hidden', 'hidden'), ('archived', 'archived'), ('deleted', 'deleted')], default='published', max_length=100, no_check_for_status=True)),
                ('title', models.CharField(max_length=250)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_comments', to='blog_module.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_comments', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog_module.comment')),
            ],
        ),
    ]
