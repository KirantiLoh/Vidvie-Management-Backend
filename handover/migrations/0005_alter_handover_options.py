# Generated by Django 4.0.6 on 2022-07-19 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handover', '0004_alter_handover_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='handover',
            options={'ordering': ('-date_added',)},
        ),
    ]