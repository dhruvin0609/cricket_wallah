# Generated by Django 4.1.7 on 2023-03-27 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0004_rename_socre1_livematch_score1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='livematch',
            name='win',
            field=models.IntegerField(default=0),
        ),
    ]
