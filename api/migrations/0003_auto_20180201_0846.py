# Generated by Django 2.0.1 on 2018-02-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180201_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.CharField(default='no date', max_length=10),
        ),
    ]
