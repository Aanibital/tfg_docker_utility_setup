# Generated by Django 3.2.12 on 2022-06-07 15:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eventlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='completed',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
