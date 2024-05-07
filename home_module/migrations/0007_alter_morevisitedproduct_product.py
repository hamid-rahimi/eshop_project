# Generated by Django 4.2 on 2024-04-24 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0001_initial'),
        ('home_module', '0006_alter_morevisitedproduct_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='morevisitedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visited_product', to='product_module.product'),
        ),
    ]
