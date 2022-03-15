from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="homepage.html"),),
    path('schedule/', include('schedule.urls')),
    path('fullcalendar/', TemplateView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),
]