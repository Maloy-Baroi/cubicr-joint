# Generated by Django 4.0.5 on 2022-06-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_auth', '0008_referencesmodel_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencesmodel',
            name='created',
            field=models.DateField(auto_now=True),
        ),
    ]
