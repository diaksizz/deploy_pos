# Generated by Django 3.0.7 on 2020-07-08 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20200708_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbarang',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
