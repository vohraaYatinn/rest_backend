# Generated by Django 5.1.2 on 2024-11-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0021_orderitem_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="rating",
            field=models.IntegerField(default=0),
        ),
    ]