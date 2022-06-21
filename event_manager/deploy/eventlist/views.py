# Django imports
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

# Django rest framework imports
from rest_framework import viewsets
from rest_framework import permissions

# Event list imports
from .forms import LoginForm, SignUpForm, addEventForm, addListForm, EditListForm, EditEventForm
from .models import User, Event, EventList
from .serializers import EventListSerializer, EventSerializer



def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is None:
                return render(request, "accounts/login.html", {"form": form, "msg": 'Invalid credentials'})

            # If is the first time a user logs create his profile
            try:
                profile = User.objects.all().get(user = user)
            except ObjectDoesNotExist:
                profile = User(user = user)
                profile.save()

            login(request, user)
            return redirect('list_event_lists')

    return render(request, "accounts/login.html", {"form": form, "msg": 'Error validating the form'})

def index(request):
    return render(request,"home/index.html")

@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    return render(request,"accounts/logout.html")

@login_required(login_url='/accounts/login/')
def list_event_lists(request):

    user, created = User.objects.get_or_create(user=request.user)
    if request.method == "GET":
        form = addListForm()
        return render(
            request,
            "home/list_event_lists.html",
            {
                "form": form,
                "lists": user.eventlist_set.all()
            }
        )
    
    if request.method == 'POST':
        if not request.user.has_perm('eventlist.add_eventlist'):
            return render(request,"home/403.html")
        form = addListForm(request.POST)
        if form.is_valid():
            event_list = EventList(
                name = form.cleaned_data['name'],
            )
            event_list.save()
            event_list.users.add(User.objects.get(user_id = request.user.id))
            event_list.save()
        return redirect(list_event_lists)


@login_required(login_url='/accounts/login/')
def detail_event_list(request, list_name):


    user, created = User.objects.get_or_create(user=request.user)
    event_list = get_object_or_404(EventList, name = list_name)

    if user not in event_list.users.all():
        return render(request,"home/403.html")

    if request.method == 'GET': 
        form = addEventForm()
        return render(
            request,
            "home/event_list.html",
            {
                "form": form,
                "list": event_list,
            }
        )

    if request.method == 'POST':
        if not request.user.has_perm('eventlist.add_event'):
            return render(request,"home/403.html")
        form = addEventForm(request.POST)
        if form.is_valid():
            event = Event(
                name = form.cleaned_data['name'],
                date = form.cleaned_data['date'],
                description = form.cleaned_data['description'],
                event_list = event_list,
                creator = User.objects.get(user_id = request.user.id)
            )
            event.save()
        return redirect('list_events', list_name = list_name)


@login_required(login_url='/accounts/login/')
def profile(request):

    user, created = User.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        return render(
            request,
            'home/profile.html',
            {
                'change_password_form':PasswordChangeForm(request.user),
                'profile': user,
                'events':Event.objects.all().filter(creator = user).order_by('-creation_date')
            }
        )
    if request.method == 'POST':
        if not request.user.has_perm('eventlist.change_user'):
            return render(request,"home/403.html")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')

@login_required(login_url='/accounts/login/')
def delete_list_confirmation(request, list_name):
    
    if not request.user.has_perm('eventlist.delete_eventlist'):
            return render(request,"home/403.html")
    event_list = get_object_or_404(EventList, name = list_name)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    if(event_list in user.eventlist_set.all()):
        return render(
            request,
            "home/delete_list_confirmation.html",
            {
                "list": event_list,
            }
        )


@login_required(login_url='/accounts/login/')
def delete_list(request, list_name):

    if not request.user.has_perm('eventlist.delete_eventlist'):
            return render(request,"home/403.html")
    event_list = get_object_or_404(EventList, name = list_name)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    event_list.delete()
    return redirect('list_event_lists')

@login_required(login_url='/accounts/login/')
def detail_list(request, list_name):

    if not request.user.has_perm('eventlist.change_eventlist'):
            return render(request,"home/403.html")
    event_list = get_object_or_404(EventList, name = list_name)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    if request.method == 'GET':
        form = EditListForm(instance = event_list)
        return render(request, 'home/detail_list.html', {'form':form, 'list':event_list})
    if request.method == 'POST':
        form = EditListForm(request.POST, instance = event_list)
        if 'users' not in request.POST:
            return render(request, 'home/detail_list.html', {'form':form, 'list':event_list, 'error': 'You should choose at least one user, otherwise delete the list.'})
        form.save()
    return redirect('list_event_lists')

@login_required(login_url='/accounts/login/')
def detail_event(request, list_name, event_id):

    if not request.user.has_perm('eventlist.change_event'):
        return render(request,"home/403.html")
    event_list = get_object_or_404(EventList, name = list_name)
    event = get_object_or_404(Event, id = event_id)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    if event.event_list.id != event_list.id:
        return render(request, 'home/403.html')

    if request.method == 'GET':
        form = EditEventForm(instance = event)
        return render(request, 'home/event_detail.html', {'form':form, 'event':event})
    if request.method == 'POST':
        form = EditEventForm(request.POST, instance = event)
        form.save()
        event = get_object_or_404(Event, id = event_id)
        if 'completed' in request.POST :
            event.completed = True
            event.save()
        else:
            event.completed = False
            event.save()

    return redirect('list_events', list_name = event_list.name) 

@login_required(login_url='/accounts/login/')
def delete_event(request, list_name, event_id):
    
    if not request.user.has_perm('eventlist.delete_event'):
        return render(request,"home/403.html")
    event_list = get_object_or_404(EventList, name = list_name)
    event = get_object_or_404(Event, id = event_id)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    event.delete()
    
    return redirect('list_events', list_name = list_name)


@login_required(login_url='/accounts/login/')
def check_event(request, list_name, event_id):
    
    if not request.user.has_perm('eventlist.change_event'):
        return render(request,"home/403.html")
    event_list = get_object_or_404(EventList, name = list_name)
    event = get_object_or_404(Event, id = event_id)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    event.mark_as_completed(request.user.username)

    return redirect('list_events', list_name = list_name)
    
# REST interface views
class EventListViewSet(viewsets.ModelViewSet):
    queryset = EventList.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


# Error hadler
def page_not_found_view(request, exception):
    return render(request, 'home/404.html', status=404)
