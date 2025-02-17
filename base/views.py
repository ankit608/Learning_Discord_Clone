from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, Topic , Message
from .forms import RoomForm , UserForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    print(rooms)
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_message':room_message}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by
    participants = room.participants.all()
    print(participants,"here participants will be shown")

    if(request.method=="POST"):
        messages= Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context = {'room': room,'room_messages': room_messages, 'participants': participants}
    print(context)
    return render(request, 'base/Room.html', context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url ="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    print(pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are Not allowed to delete or update')
    if request.method == 'POST':
            topic_name = request.POST.get('topic')
            topic,created = Topic.objects.get_or_create(name= topic_name)
            room.name = request.POST.get('name')
            room.topic = topic
            room.description = request.POST.get('description')
            room.save()
            return redirect('home')
    context = {'form': form,'topics':topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url ="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html.', {'obj': room})


def LoginPage(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        print(username,password)

        try:
            user = User.objects.get(username=username)
        except:
            print("hellooo")
            messages.error(request, 'Document does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'useranme or password does not exist')

    context = {'page':page}
    return render(request, 'base/Login_Registration.html', context)
@login_required(login_url ="login")
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'base/Login_Registration.html',{'form':form})

def deleteMessage(request,pk):
     message = Message.objects.get(id=pk)

     if request.user != message.user:
        return HttpResponse("you are not allowed here !!")
     if request.method == 'POST':
         message.delete()
         return redirect('home')
     return render(request,'base/delete.html',{'obj':message})


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_message':room_message}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request,'base/update-user.html', {'form': form})



"""form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()"""