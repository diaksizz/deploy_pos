# Generated by Django 3.0.7 on 2020-06-27 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20200627_0803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rekaptransaksi',
            name='harga',
        ),
    ]