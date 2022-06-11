from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from .forms import LoginForm, SignUpForm, addEventForm, addListForm
from .models import User, Event, EventList

import datetime

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            # If is the first time a user logs create his profile
            try:
                profile = User.objects.all().get(user = user)
            except ObjectDoesNotExist:
                profile = User(user = user)
                profile.save()

            if user is not None:
                login(request, user)
                return redirect('list_event_lists')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def index(request):
    return render(request,"home/index.html")

@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    return render(request,"accounts/logout.html")

@login_required(login_url='/accounts/login/')
def list_event_lists(request):

    user, created = User.objects.get_or_create(user=request.user)
    print(user)
    if request.method == "GET":
        form = addListForm()
        print(User._meta.get_fields())
        return render(
            request,
            "home/list_event_lists.html",
            {
                "form": form,
                "lists": user.eventlist_set.all()
            }
        )
    
    if request.method == 'POST':
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

    user = User.objects.get_or_create(user=request.user)
    event_list = get_object_or_404(EventList, name = list_name)

    if user in event_list.users.all():
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
def detail_event(request, list_name, event_name):

    event_list = get_object_or_404(EventList, name = list_name)
    event = get_object_or_404(Event, name = event_name)

    if request.method == "GET":
       
        return render(
            request,
            "home/event_detail.hmtl",
            {
                "list": event_list,
                "event": event,
            }
        )

@login_required(login_url='/accounts/login/')
def profile(request):

    user, created = User.objects.get_or_create(user=request.user)

    if request.method == "GET":
       
        return render(
            request,
            "home/profile.html",
            {
                "profile": user,
            }
        )

@login_required(login_url='/accounts/login/')
def delete_list_confirmation(request, list_name):
    
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

    event_list = get_object_or_404(EventList, name = list_name)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    event_list.delete()
    return redirect('list_event_lists')

@login_required(login_url='/accounts/login/')
def delete_event(request, list_name, event_id):
    
    event_list = get_object_or_404(EventList, name = list_name)
    event = get_object_or_404(Event, id = event_id)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    event.delete()
    
    return redirect('list_events', list_name = list_name)


@login_required(login_url='/accounts/login/')
def check_event(request, list_name, event_id):
    # TODO:Check for the permission and membership of the user 

    event_list = get_object_or_404(EventList, name = list_name)
    event = get_object_or_404(Event, id = event_id)
    user, created = User.objects.get_or_create(user=request.user)

    if created or not event_list.users.filter(id=user.id).exists():
        return render(request, 'home/403.html')

    event.mark_as_completed(request.user.username)

    return redirect('list_events', list_name = list_name)
    


