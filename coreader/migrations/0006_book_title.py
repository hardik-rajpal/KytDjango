# Generated by Django 3.2.7 on 2022-06-21 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreader', '0005_alter_userprofile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='title',
            field=models.CharField(default='', max_length=300),
        ),
    ]