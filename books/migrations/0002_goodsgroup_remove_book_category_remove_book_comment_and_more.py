# Generated by Django 5.0 on 2023-12-25 03:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoodsGroup",
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
                (
                    "name",
                    models.CharField(
                        max_length=10, null=True, unique=True, verbose_name="商品グループ"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="book",
            name="category",
        ),
        migrations.RemoveField(
            model_name="book",
            name="comment",
        ),
        migrations.RemoveField(
            model_name="book",
            name="posted_at",
        ),
        migrations.RemoveField(
            model_name="book",
            name="title",
        ),
        migrations.AddField(
            model_name="book",
            name="description",
            field=models.CharField(
                default="default_description", max_length=100000, verbose_name="説明"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="management_code",
            field=models.CharField(
                default="default_code", max_length=20, unique=True, verbose_name="管理コード"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="name",
            field=models.CharField(max_length=100, null=True, verbose_name="商品名"),
        ),
        migrations.AddField(
            model_name="book",
            name="price",
            field=models.IntegerField(default=0, verbose_name="価格"),
        ),
        migrations.AddField(
            model_name="book",
            name="release_date",
            field=models.DateField(blank=True, null=True, verbose_name="発売日"),
        ),
        migrations.AddField(
            model_name="book",
            name="release_flag",
            field=models.BooleanField(default=False, verbose_name="発売済み"),
        ),
        migrations.AlterField(
            model_name="book",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="goods_image/", verbose_name="イメージ"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="books.goodsgroup",
                verbose_name="商品グループ",
            ),
        ),
    ]