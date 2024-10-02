from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model, authenticate

from user.forms import LoginForm, RegisterForm
from .models import Profile


def login(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main')

    return render(request, 'user/login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('main')


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('Надо создать пользователя')

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # созадли пользователя
            User = get_user_model()
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user)

            user = authenticate(request, username=username, password=password)
            auth_login(request=request, user=user)

            return redirect('notes')

    return render(request, 'user/register.html', {'form': form})


@login_required
def home(request):
    profile = request.user.profile

    notes = profile.profile_notes.all()

    # # альтернатиный вариант получения постов пользователя
    # posts = Post.objects.filter(profile=profile)

    return render(request, 'user/home.html', {'notes': notes})
