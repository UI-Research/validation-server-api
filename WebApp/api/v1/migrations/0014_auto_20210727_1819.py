# Generated by Django 3.1.4 on 2021-07-27 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0013_command_command_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command_title',
            field=models.CharField(default='Command_title', max_length=100),
        ),
    ]
