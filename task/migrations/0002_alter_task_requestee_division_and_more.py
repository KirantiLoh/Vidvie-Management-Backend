# Generated by Django 4.0.4 on 2022-05-18 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_division_leader'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='requestee_division',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='user.division'),
        ),
        migrations.AlterField(
            model_name='task',
            name='requestor_division',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='user.division'),
        ),
    ]
