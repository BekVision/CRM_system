# Generated by Django 5.2.1 on 2025-05-13 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customers',
            options={},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={},
        ),
        migrations.AlterModelOptions(
            name='orderitems',
            options={},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={},
        ),
        migrations.AlterModelOptions(
            name='payments',
            options={},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={},
        ),
        migrations.AlterModelOptions(
            name='shipments',
            options={},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='inventory',
            name='quantity_in_stock',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='quantity_reserved',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='reorder_level',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orders',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payments',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
