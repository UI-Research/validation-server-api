# Generated by Django 3.1.4 on 2021-09-03 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0020_auto_20210818_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='confidentialdataresult',
            name='original_display_results_decision',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='confidentialdataresult',
            name='original_release_results_decision',
            field=models.BooleanField(default=False),
        ),
    ]
