# Generated by Django 5.1.2 on 2024-10-15 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_order_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="image",
        ),
    ]
