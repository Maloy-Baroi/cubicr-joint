# Generated by Django 4.0.5 on 2022-06-20 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_auth', '0009_alter_referencesmodel_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_main',
            name='career_objective',
            field=models.TextField(default="Opportunities don't happen, You create them. "),
        ),
    ]
