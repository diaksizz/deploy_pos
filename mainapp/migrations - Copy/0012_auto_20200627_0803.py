# Generated by Django 3.0.7 on 2020-06-27 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20200622_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='rekaptransaksi',
            name='harga_beli',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rekaptransaksi',
            name='harga_jual',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='idtrx',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
