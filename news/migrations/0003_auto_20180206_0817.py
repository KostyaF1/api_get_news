# Generated by Django 2.0.1 on 2018-02-06 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_remove_new_post_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='new_post',
            name='score',
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.New_Post'),
        ),
    ]
