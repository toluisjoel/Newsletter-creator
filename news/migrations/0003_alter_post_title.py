# Generated by Django 4.1 on 2022-10-14 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
