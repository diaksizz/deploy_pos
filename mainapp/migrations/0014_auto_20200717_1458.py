# Generated by Django 3.0.8 on 2020-07-17 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20200717_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
