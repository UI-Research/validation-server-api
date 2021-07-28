# Generated by Django 3.1.4 on 2021-07-28 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0015_auto_20210727_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='researcher_id',
            field=models.ForeignKey(db_column='researcher_id', on_delete=django.db.models.deletion.CASCADE, related_name='commands', to=settings.AUTH_USER_MODEL),
        ),
    ]