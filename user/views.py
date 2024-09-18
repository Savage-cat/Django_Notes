from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout

from user.forms import LoginForm


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
