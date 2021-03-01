# Generated by Django 3.1.4 on 2021-01-07 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0002_delete_run'),
    ]

    operations = [
        migrations.CreateModel(
            name='Run',
            fields=[
                ('run_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('run_type', models.IntegerField(choices=[(1, 'OLS'), (2, 'Tabulation')])),
                ('sanitized_run_input', models.JSONField()),
                ('display_results_decision', models.BooleanField(default=False)),
                ('display_results_number', models.IntegerField(default=1)),
                ('date_time_run_submitted', models.DateTimeField(auto_now_add=True)),
                ('researcher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
