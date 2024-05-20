# Generated by Django 4.2.11 on 2024-05-15 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_verified_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="audit",
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterField(
            model_name="audit",
            name="event",
            field=models.CharField(
                choices=[("login", "login"), ("logout", "logout"), ("password_reset", "Password Reset")], max_length=255
            ),
        ),
    ]
