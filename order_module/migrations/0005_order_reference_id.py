# Generated by Django 4.2 on 2024-05-05 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0004_alter_orderitem_payment_amount_for_once'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reference_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='شماره پی گیری'),
        ),
    ]
