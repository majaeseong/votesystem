# Generated by Django 2.0.9 on 2018-12-30 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='name',
        ),
    ]
