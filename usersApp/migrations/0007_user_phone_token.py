# Generated by Django 5.1.2 on 2024-12-16 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usersApp", "0006_address_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone_token",
            field=models.TextField(blank=True, null=True),
        ),
    ]
