# Generated by Django 4.1.7 on 2023-03-27 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0005_livematch_win'),
    ]

    operations = [
        migrations.AddField(
            model_name='livematch',
            name='current_ball',
            field=models.IntegerField(default=0),
        ),
    ]
