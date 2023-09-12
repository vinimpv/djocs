# Generated by Django 4.2.4 on 2023-09-08 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_historicalknowledge_category_knowledge_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalknowledge",
            name="category",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="core.knowledgecategory",
            ),
        ),
        migrations.AlterField(
            model_name="knowledge",
            name="category",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.knowledgecategory"
            ),
        ),
    ]
