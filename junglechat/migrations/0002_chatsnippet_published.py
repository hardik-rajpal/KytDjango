# Generated by Django 3.2.6 on 2021-10-15 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('junglechat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsnippet',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]