# Generated by Django 4.0.5 on 2022-06-19 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postlovereact',
            name='liked',
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='topic_name',
            field=models.CharField(default='None', max_length=100),
            preserve_default=False,
        ),
    ]
