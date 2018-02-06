# Generated by Django 2.0.1 on 2018-02-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20180206_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=15)),
                ('url', models.CharField(max_length=200)),
                ('item_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SiteObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=20)),
                ('site_items', models.ManyToManyField(to='news.NewPost')),
            ],
        ),
        migrations.RemoveField(
            model_name='sitemodel',
            name='items',
        ),
        migrations.DeleteModel(
            name='New_Post',
        ),
        migrations.DeleteModel(
            name='SiteModel',
        ),
    ]
