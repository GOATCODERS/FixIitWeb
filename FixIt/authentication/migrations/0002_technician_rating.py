# Generated by Django 5.1.3 on 2025-03-08 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='technician',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
