# Generated by Django 3.0.7 on 2020-06-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20200620_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='barang',
            old_name='harga',
            new_name='harga_beli',
        ),
        migrations.AddField(
            model_name='barang',
            name='harga_jual',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]