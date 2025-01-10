# Generated by Django 5.1.2 on 2024-11-28 11:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointments', '0001_initial'),
        ('reports', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='report',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='reports.report'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident_appointments', to=settings.AUTH_USER_MODEL),
        ),
    ]
