# Generated by Django 2.0.1 on 2018-02-06 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20180206_0817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitemodel',
            name='name',
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='items',
            field=models.ManyToManyField(to='news.New_Post'),
        ),
    ]