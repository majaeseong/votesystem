# Generated by Django 2.0.9 on 2019-01-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_auto_20181231_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
            ],
        ),
    ]