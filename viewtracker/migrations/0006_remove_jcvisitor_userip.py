# Generated by Django 3.2.6 on 2021-10-08 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewtracker', '0005_remove_kytvisitor_userip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jcvisitor',
            name='userip',
        ),
    ]
