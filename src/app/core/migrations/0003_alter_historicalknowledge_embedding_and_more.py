# Generated by Django 4.2.4 on 2023-09-03 12:41

from django.db import migrations
import pgvector.django


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_historicalmessage_embedding_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalknowledge",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True),
        ),
        migrations.AlterField(
            model_name="historicalresponse",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True),
        ),
        migrations.AlterField(
            model_name="knowledge",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True),
        ),
        migrations.AlterField(
            model_name="response",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=1536, null=True),
        ),
    ]
