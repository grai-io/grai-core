# Generated by Django 4.1.3 on 2022-12-12 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("connections", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="connections",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
