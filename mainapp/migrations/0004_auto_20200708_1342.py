# Generated by Django 3.0.7 on 2020-07-08 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20200708_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='rekaptransaksi',
            name='harga',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rekaptransaksi',
            name='supplier',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rekaptransaksi',
            name='barang',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
