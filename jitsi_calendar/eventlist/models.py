from django.db import models
from django.contrib.auth.models import User as DjangoUser

class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, username, email, password):
        user = DjangoUser.objects.create_user(username = username, email = email, password = password)
        return cls(user = user)

    def __str__(self) -> str:
        return self.user.username

class EventList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, blank = True)

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    event_list = models.ForeignKey(EventList, unique = False, on_delete=models.CASCADE)
    description = models.TextField()
    creator = models.ForeignKey(User, unique = False, on_delete=models.PROTECT)
    date = models.DateTimeField()
    creation_date = models.DateField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False, blank = True)
    notes = models.TextField()

    def __str__(self) -> str:
        return self.name + ' ' + str(self.date)



