from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from rest_framework import routers

from eventlist import views as event_list_view

router_drf = routers.DefaultRouter()
router_drf.register(r'eventlist', event_list_view.EventListViewSet)
router_drf.register(r'event', event_list_view.EventViewSet)


urlpatterns = [
    # Admin 
    path('admin/', admin.site.urls),
    # Accounts
    path('accounts/login/', event_list_view.login_view, name="login"),
    path('accounts/logout/', event_list_view.logout_view, name="logout"),
    path('accounts/profile/', event_list_view.profile, name="profile"),
    # Web app
    path('', event_list_view.index, name='index'),
    path('events/', event_list_view.list_event_lists, name='list_event_lists'),
    path('events/<str:list_name>/', event_list_view.detail_event_list, name='list_events'),
    path('events/<str:list_name>/<int:event_id>/', event_list_view.detail_event, name='detail_event'),
    path('events/<str:list_name>/delete', event_list_view.delete_list, name='delete_list'),
    path('events/<str:list_name>/edit', event_list_view.edit_list, name='edit_list'),
    path('events/<str:list_name>/delete/confirmation', event_list_view.delete_list_confirmation, name='delete_list_confirmation'),
    path('events/<str:list_name>/delete/<int:event_id>', event_list_view.delete_event, name='delete_event'),
    path('events/<str:list_name>/check/<int:event_id>', event_list_view.check_event, name='check_event'),
    # Api  
    path('api/', include(router_drf.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

handler404 = "eventlist.views.page_not_found_view"