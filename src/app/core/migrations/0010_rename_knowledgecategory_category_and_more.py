# Generated by Django 4.2.4 on 2023-09-10 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0009_chat_is_template_historicalchat_is_template"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="KnowledgeCategory",
            new_name="Category",
        ),
        migrations.RenameModel(
            old_name="HistoricalKnowledgeCategory",
            new_name="HistoricalCategory",
        ),
        migrations.AlterModelOptions(
            name="historicalcategory",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical category",
                "verbose_name_plural": "historical categorys",
            },
        ),
        migrations.RemoveField(
            model_name="category",
            name="parent_category",
        ),
        migrations.RemoveField(
            model_name="historicalcategory",
            name="parent_category",
        ),
        migrations.AddField(
            model_name="category",
            name="user",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="chat",
            name="category",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.category"
            ),
        ),
        migrations.AddField(
            model_name="historicalcategory",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalchat",
            name="category",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="core.category",
            ),
        ),
    ]
