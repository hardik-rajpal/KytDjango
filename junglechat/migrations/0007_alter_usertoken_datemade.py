# Generated by Django 3.2.6 on 2022-02-26 06:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('junglechat', '0006_auto_20220226_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='dateMade',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]
