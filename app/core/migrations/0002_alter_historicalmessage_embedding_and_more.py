# Generated by Django 4.2.4 on 2023-09-03 12:41

from django.db import migrations
import pgvector.django


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalmessage",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True),
        ),
        migrations.AlterField(
            model_name="message",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True),
        ),
    ]
