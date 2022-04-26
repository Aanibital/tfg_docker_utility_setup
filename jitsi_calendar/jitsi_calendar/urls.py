from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from eventlist import views as event_list_view

urlpatterns = [
    # Admin 
    path('accounts/admin/', admin.site.urls),
    # Accounts
    path('accounts/login/', event_list_view.login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # Web app
    path('events/', event_list_view.list_event_lists, name='list_event_lists'),
    path('events/<str:list_name>/', event_list_view.detail_event_list, name='list_events'),
    path('events/<str:list_name>/<str:event_name>', event_list_view.detail_event, name='detail_event'),
    # Api  
]

