# Generated by Django 3.1.5 on 2021-03-12 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20210311_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting_room',
            name='name',
            field=models.CharField(default='default_value', max_length=150),
        ),
    ]
