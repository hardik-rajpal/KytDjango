# Generated by Django 3.2.6 on 2021-10-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userip', models.GenericIPAddressField()),
                ('freq', models.IntegerField()),
                ('loc', models.CharField(max_length=300)),
            ],
        ),
    ]
