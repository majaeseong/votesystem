# Generated by Django 2.0.9 on 2019-01-06 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_noti_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noti',
            name='read',
        ),
    ]