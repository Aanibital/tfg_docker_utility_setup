from django.db import models
from django.contrib.auth.models import User as DjangoUser

class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username

class Meeting(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.IntegerField()
    participants = models.ManyToManyField(User)
    meeting_date = models.DateTimeField()
    creation_date = models.DateField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name + ' ' + self.meeting_date

