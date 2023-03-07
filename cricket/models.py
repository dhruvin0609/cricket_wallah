from django.db import models

# Create your models here.


class team(models.Model):
    teamname = models.CharField(max_length=40)


class player(models.Model):
    playername = models.CharField(max_length=100)
