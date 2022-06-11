from django.contrib import admin
from .models import Event, EventList, User

admin.site.register(Event)
admin.site.register(EventList)
admin.site.register(User)
