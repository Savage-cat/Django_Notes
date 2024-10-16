from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from core.models import Note, Favorites
from user.models import Profile


def test(request):

    return JsonResponse({"status": "OK"})


def ajax(request):

    return JsonResponse({"status": "OK", 'message': 'test request'})


@login_required
def favorites(request, profile_id):

    redirect_url = request.GET.get('next')
    author = Profile.objects.get(id=profile_id)
    profile = request.user.profile

    Favorites.objects.get_or_create(author=author, profile=profile)

    return JsonResponse({"status": "OK"})

@login_required
def unfavorites(request, profile_id):

    redirect_url = request.GET.get('next')
    author = Profile.objects.get(id=profile_id)
    profile = request.user.profile

    Favorites.objects.filter(author=author, profile=profile).delete()

    return JsonResponse({"status": "OK"})