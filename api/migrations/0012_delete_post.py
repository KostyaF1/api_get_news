# Generated by Django 2.0.1 on 2018-02-06 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_post_pub_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
