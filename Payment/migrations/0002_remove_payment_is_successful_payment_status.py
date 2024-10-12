# Generated by Django 5.0.1 on 2024-10-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='is_successful',
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('PENDING', 'Pending')], default='PENDING', max_length=10),
        ),
    ]
