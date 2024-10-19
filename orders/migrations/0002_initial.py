# Generated by Django 5.1.2 on 2024-10-11 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("menu", "0001_initial"),
        ("orders", "0001_initial"),
        ("usersApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="usersApp.address"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="usersApp.user"
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="menu.menuitem"
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="orders.order",
            ),
        ),
    ]
