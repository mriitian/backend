# Generated by Django 5.0.6 on 2024-06-26 17:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='pick_date',
            new_name='appointment_date',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='pick_time',
            new_name='appointment_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='service_required',
            field=models.CharField(choices=[('Service1', 'Service 1'), ('Service2', 'Service 2'), ('Service3', 'Service 3')], max_length=50),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]