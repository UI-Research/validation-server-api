# Generated by Django 3.1.4 on 2021-07-28 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0016_auto_20210728_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confidentialdataresult',
            name='command_id',
            field=models.ForeignKey(db_column='command_id', on_delete=django.db.models.deletion.CASCADE, to='v1.command'),
        ),
        migrations.AlterField(
            model_name='confidentialdataresult',
            name='run_id',
            field=models.OneToOneField(db_column='run_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='v1.confidentialdatarun'),
        ),
        migrations.AlterField(
            model_name='confidentialdatarun',
            name='command_id',
            field=models.ForeignKey(db_column='command_id', on_delete=django.db.models.deletion.CASCADE, to='v1.command'),
        ),
        migrations.AlterField(
            model_name='publicusebudget',
            name='researcher_id',
            field=models.OneToOneField(db_column='researcher_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reviewandrefinementbudget',
            name='researcher_id',
            field=models.OneToOneField(db_column='researcher_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='syntheticdataresult',
            name='command_id',
            field=models.ForeignKey(db_column='command_id', on_delete=django.db.models.deletion.CASCADE, to='v1.command'),
        ),
        migrations.AlterField(
            model_name='syntheticdataresult',
            name='run_id',
            field=models.OneToOneField(db_column='run_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='v1.syntheticdatarun'),
        ),
        migrations.AlterField(
            model_name='syntheticdatarun',
            name='command_id',
            field=models.ForeignKey(db_column='command_id', on_delete=django.db.models.deletion.CASCADE, to='v1.command'),
        ),
    ]
