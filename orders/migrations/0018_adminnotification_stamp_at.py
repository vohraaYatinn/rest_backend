# Generated by Django 5.1.2 on 2024-11-04 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0017_alter_notificationuser_user_alter_order_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="adminnotification",
            name="stamp_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
