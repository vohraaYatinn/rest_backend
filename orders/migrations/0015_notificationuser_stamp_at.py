# Generated by Django 5.1.2 on 2024-10-30 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0014_remove_notificationuser_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="notificationuser",
            name="stamp_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
