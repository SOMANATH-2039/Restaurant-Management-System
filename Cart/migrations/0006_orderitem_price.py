# Generated by Django 5.0.1 on 2024-10-08 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0005_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
