from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from core.forms import FeedbackForm
from core.models import Note, Favorites, NoteComment
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

    return JsonResponse({"message": "добавлено в избранное"})

@login_required
def unfavorites(request, profile_id):

    redirect_url = request.GET.get('next')
    author = Profile.objects.get(id=profile_id)
    profile = request.user.profile

    Favorites.objects.filter(author=author, profile=profile).delete()

    return JsonResponse({"status": "OK"})


def feedback(request):
    """Обработка аякс запроса"""

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()

            return JsonResponse({"message": "Обратная связь отправлена"})
        else:
            return JsonResponse({'errors': form.errors}, status=400)


def note_comments(request, note_id):
    note = Note.objects.get(id=note_id)
    comments = NoteComment.objects.filter(note=note)

    new_comments = []

    for comment in comments:
        new_comments.append({
            'text': comment.text,
            'profile': comment.profile.user.username
        })

    return JsonResponse({"comments": new_comments}, safe=False)


def film_add(request):

    # Выводим данные формы
    print(request.POST)

    # вот здесь происходит обработка формы

    return redirect('vue')