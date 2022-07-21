# Generated by Django 4.0.6 on 2022-07-18 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handover', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='handover',
            name='tipe',
            field=models.CharField(choices=[('Peminjaman', 'Peminjaman'), ('Pengembalian', 'Pengembalian'), ('Permintaan', 'Permintaan')], default='', max_length=50),
            preserve_default=False,
        ),
    ]