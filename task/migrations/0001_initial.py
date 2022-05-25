# Generated by Django 4.0.4 on 2022-05-18 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=1000)),
                ('priority', models.CharField(choices=[('HIGH', 'High'), ('MED', 'Medium'), ('LOW', 'Low')], max_length=10)),
                ('status', models.CharField(choices=[('NOT_STARTED', 'Not Started'), ('IN_PROGRESS', 'In Progress'), ('SHIPPING', 'Shipping'), ('FINISHED', 'Finished')], max_length=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateTimeField()),
                ('requestee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='user.account')),
                ('requestee_division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='user.division')),
                ('requestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='user.account')),
                ('requestor_division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='user.division')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
    ]
