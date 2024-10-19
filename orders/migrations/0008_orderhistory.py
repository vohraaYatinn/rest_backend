# Generated by Django 5.1.2 on 2024-10-16 07:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0007_alter_order_ordered_at_alter_orderitem_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("delivered", "Delivered"),
                            ("cancelled", "Cancelled"),
                            ("Ondelivery", "Ondelivery"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("stamp_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_history",
                        to="orders.order",
                    ),
                ),
            ],
        ),
    ]
