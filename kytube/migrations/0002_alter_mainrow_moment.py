# Generated by Django 3.2.6 on 2021-09-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kytube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainrow',
            name='moment',
            field=models.CharField(max_length=100),
        ),
    ]
