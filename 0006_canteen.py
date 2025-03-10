# Generated by Django 5.1.3 on 2024-11-26 08:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("canteen", "0005_earnings"),
    ]

    operations = [
        migrations.CreateModel(
            name="Canteen",
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
                ("name", models.CharField(max_length=100)),
                (
                    "total_earnings",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
            ],
        ),
    ]
