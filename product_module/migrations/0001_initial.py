# Generated by Django 4.2 on 2024-04-05 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='brand')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='title')),
                ('price', models.IntegerField(verbose_name='price')),
                ('short_description', models.CharField(max_length=500, null=True, verbose_name='short description')),
                ('description', models.TextField(verbose_name='description')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is delete')),
                ('slug', models.SlugField(default='', unique=True, verbose_name='slug')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d/', verbose_name='image')),
                ('brands', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products_brand', to='product_module.brand', verbose_name='products brand')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(db_index=True, max_length=250, verbose_name='caption')),
                ('product_tags', models.ManyToManyField(related_name='product_tags', to='product_module.product', verbose_name='product tags')),
            ],
            options={
                'verbose_name': 'product tag',
                'verbose_name_plural': 'product tags',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='title')),
                ('url_title', models.CharField(db_index=True, max_length=200, verbose_name='url title')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is delete')),
                ('categories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.productcategory', verbose_name='categories')),
            ],
            options={
                'verbose_name': 'product category',
                'verbose_name_plural': 'product categories',
                'db_table': 'category',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ManyToManyField(related_name='product_categories', to='product_module.productcategory', verbose_name='product category'),
        ),
    ]