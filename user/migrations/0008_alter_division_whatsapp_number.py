# Generated by Django 4.0.4 on 2022-05-25 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_division_whatsapp_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
