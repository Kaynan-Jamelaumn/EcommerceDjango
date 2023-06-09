# Generated by Django 3.2.13 on 2023-04-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_productvariation_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(blank=True, to='product.SubCategory'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='subsubcategory',
        ),
        migrations.AddField(
            model_name='product',
            name='subsubcategory',
            field=models.ManyToManyField(blank=True, to='product.SubSubCategory'),
        ),
    ]
