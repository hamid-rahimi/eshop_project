# Generated by Django 4.2 on 2024-04-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0006_userprofile_address_userprofile_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
