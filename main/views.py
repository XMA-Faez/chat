from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import SignUpForm, FindUserForm
from .models import UserProfile, ChatRoom, Message


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile is created automatically by signal in signals.py
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


@login_required
def home_view(request):
    chat_rooms = request.user.chat_rooms.all()
    
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    chat_data = []
    for room in chat_rooms:
        other_user = room.get_other_user(request.user)
        last_message = room.messages.last()
        unread_count = room.messages.filter(sender=other_user, is_read=False).count()
        
        chat_data.append({
            'room': room,
            'other_user': other_user,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    context = {
        'chat_data': chat_data,
        'user_profile': user_profile
    }
    return render(request, 'main/home.html', context)


@login_required
def find_user_view(request):
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    form = FindUserForm()
    error_message = None
    
    if request.method == 'POST':
        form = FindUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                target_user = User.objects.get(username=username)
                
                if target_user == request.user:
                    error_message = "You cannot chat with yourself!"
                else:
                    # Check if chat room already exists
                    existing_room = ChatRoom.objects.filter(
                        participants=request.user
                    ).filter(
                        participants=target_user
                    ).first()
                    
                    if existing_room:
                        return redirect('chat_room', room_id=existing_room.id)
                    else:
                        # Create new chat room
                        new_room = ChatRoom.objects.create()
                        new_room.participants.add(request.user, target_user)
                        return redirect('chat_room', room_id=new_room.id)
                        
            except User.DoesNotExist:
                error_message = "No user found with that username."
    
    context = {
        'form': form,
        'error_message': error_message,
        'user_profile': user_profile
    }
    return render(request, 'main/find_user.html', context)


@login_required
def chat_room_view(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Verify user is participant
    if request.user not in room.participants.all():
        return redirect('home')
    
    other_user = room.get_other_user(request.user)
    messages = room.messages.all()
    
    # Mark messages as read
    room.messages.filter(sender=other_user, is_read=False).update(is_read=True)
    
    # Get or create user profiles
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    other_profile, created = UserProfile.objects.get_or_create(user=other_user)
    
    context = {
        'room': room,
        'other_user': other_user,
        'messages': messages,
        'user_profile': user_profile,
        'other_profile': other_profile
    }
    return render(request, 'main/chat_room.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')