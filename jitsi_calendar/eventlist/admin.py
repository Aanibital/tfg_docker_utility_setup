from django.contrib import admin

from .models import Event, EventList, User

admin.register(Event)
admin.register(EventList)
admin.register(User)
