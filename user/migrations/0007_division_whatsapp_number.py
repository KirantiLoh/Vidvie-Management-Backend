# Generated by Django 4.0.4 on 2022-05-24 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_division_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='whatsapp_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
