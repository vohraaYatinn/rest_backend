# Generated by Django 5.1.2 on 2024-10-18 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_remove_category_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="MenuRecommendation",
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
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommended_menu",
                        to="menu.menuitem",
                    ),
                ),
            ],
        ),
    ]
