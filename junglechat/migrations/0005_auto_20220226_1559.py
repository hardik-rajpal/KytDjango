# Generated by Django 3.2.6 on 2022-02-26 10:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('junglechat', '0004_auto_20220226_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateMade', models.DateField(auto_created=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='date',
            field=models.DateField(auto_created=True),
        ),
    ]
