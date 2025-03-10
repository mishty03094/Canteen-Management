# Generated by Django 5.1.3 on 2024-11-25 08:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("canteen", "0003_remove_order_timestamp_order_total_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivered_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="ordered_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="prepared_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("ordered", "Ordered"),
                    ("prepared", "Prepared"),
                    ("delivered", "Delivered"),
                ],
                default="ordered",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
            preserve_default=False,
        ),
    ]
