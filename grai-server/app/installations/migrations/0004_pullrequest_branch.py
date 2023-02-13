# Generated by Django 4.1.6 on 2023-02-13 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("installations", "0003_alter_branch_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pullrequest",
            name="branch",
            field=models.ForeignKey(
                default="8647f4ed-9f89-4d15-ac10-f19c2380e6f3",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pull_requests",
                to="installations.branch",
            ),
            preserve_default=False,
        ),
    ]
