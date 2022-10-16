# Generated by Django 4.1 on 2022-10-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0002_subscriber_delivered_emails_subscriber_opened_emails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='unsubscriber',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='unsubscriber',
            name='delivered_emails',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='unsubscriber',
            name='opened_emails',
            field=models.IntegerField(default=0),
        ),
    ]
