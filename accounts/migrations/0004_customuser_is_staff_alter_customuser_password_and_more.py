# Generated by Django 5.0 on 2023-12-23 15:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_remove_customuser_age_remove_customuser_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_staff",
            field=models.BooleanField(default=False, verbose_name="スタッフ権限"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(max_length=128, verbose_name="パスワード"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                error_messages={"unique": "同じユーザー名が既に登録されています"},
                max_length=100,
                unique=True,
                verbose_name="ユーザー名",
            ),
        ),
    ]
