# Generated by Django 3.1.6 on 2021-02-07 17:30
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="text",
            field=models.TextField(default=""),
        ),
    ]
