# Generated by Django 2.1.5 on 2019-01-18 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='nb_vote',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='note',
            field=models.FloatField(default=0),
        ),
    ]