# Generated by Django 4.0.6 on 2022-07-18 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handover', '0002_handover_tipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handover',
            name='count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]