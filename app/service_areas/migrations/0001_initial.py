# Generated by Django 5.1.1 on 2024-09-18 02:29

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("providers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceArea",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "geojson",
                    django.contrib.gis.db.models.fields.PolygonField(srid=4326),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_areas",
                        to="providers.provider",
                    ),
                ),
            ],
        ),
    ]
