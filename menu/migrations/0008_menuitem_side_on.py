# Generated by Django 5.1.2 on 2024-12-18 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0007_menuitem_is_buy_one"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="side_on",
            field=models.BooleanField(default=False),
        ),
    ]
