# Generated by Django 4.2 on 2023-04-14 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_products_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='description',
            field=models.TextField(help_text='Description for this product', null=True),
        ),
    ]
