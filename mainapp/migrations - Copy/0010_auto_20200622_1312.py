# Generated by Django 3.0.7 on 2020-06-22 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_transaksi_harga'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaksi',
            name='idtrx',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='harga',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='RekapTransaksi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idtrx', models.CharField(max_length=12, null=True)),
                ('status', models.CharField(max_length=200, null=True)),
                ('harga', models.IntegerField(blank=True, null=True)),
                ('qty', models.IntegerField(null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('barang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Barang')),
            ],
        ),
    ]
