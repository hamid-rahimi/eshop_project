# Generated by Django 4.2 on 2024-04-09 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('utl_title', models.CharField(max_length=250)),
                ('url', models.URLField(max_length=250)),
                ('image', models.ImageField(upload_to='sliders')),
            ],
        ),
    ]