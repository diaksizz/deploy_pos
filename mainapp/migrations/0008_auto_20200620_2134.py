# Generated by Django 3.0.7 on 2020-06-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20200620_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barang',
            name='harga_beli',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='barang',
            name='harga_jual',
            field=models.IntegerField(null=True),
        ),
    ]
