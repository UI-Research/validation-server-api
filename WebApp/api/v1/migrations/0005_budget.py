# Generated by Django 3.1.4 on 2021-01-11 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0004_auto_20210109_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('researcher_id', models.AutoField(primary_key=True, serialize=False)),
                ('budget_allocated', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('budget_used', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
