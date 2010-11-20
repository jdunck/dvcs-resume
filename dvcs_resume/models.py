from django.db import models

from django.contrib.auth.models import User

class Repo(models.Model):
    GITHUB = 1
    AUTHORITY_CHOICES = (
        (GITHUB, 'github'),
    )
    update_date = models.DateTimeField()
    authority = models.IntegerField(choices=AUTHORITY_CHOICES)
    name = models.CharField(help_text="user/repo", unique=True, null=True, blank=True, db_index=True)
    parent = models.CharField(help_text="user/repo", null=True, blank=True, db_index=True)
    peers = models.ManyToManyField(Repo) #repos from the same source (including parent?)
    watchers = models.IntegerField()
    forks = models.IntegerField()
    contributors = models.IntegerField()
    
    class Meta:
        abstract = True

class Contribution(models.Model):
    user = models.ForeignKey(User)
    repo = models.