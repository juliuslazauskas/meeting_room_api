# Generated by Django 3.1.5 on 2021-03-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20210308_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='title',
            field=models.CharField(default='', max_length=150),
        ),
    ]
