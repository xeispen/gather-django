# Generated by Django 2.0.6 on 2018-06-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gather_api', '0004_auto_20180623_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='userid',
            field=models.IntegerField(null=True),
        ),
    ]