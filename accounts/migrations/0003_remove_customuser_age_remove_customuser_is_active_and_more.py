# Generated by Django 5.0 on 2023-12-22 17:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "accounts",
            "0002_alter_customuser_options_alter_customuser_managers_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="age",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_admin",
        ),
    ]
