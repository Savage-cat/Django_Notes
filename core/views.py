from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404


from django.shortcuts import render, redirect

from user.models import Profile
from .models import Note, NoteCategory, NoteComment, Feedback, Favorites
from .forms import NoteAddForm, CommentAddForm, FeedbackForm, NoteAddModelForm

def main(request):

    note = Note.objects.all()[0]

    return render(request, 'main.html', {"note": note})


def notes(request):

    notes = Note.objects.prefetch_related('profile__user').all()

    category = request.GET.get('category')
    author = request.GET.get('author')
    order_by = request.GET.get('order_by')
    page = request.GET.get('page', 1)

    active_category = None
    active_author = None

    if category:
        # достаем посты и фильтруем
        notes = notes.filter(category__id=int(category))
        # notes = Note.objects.filter(category=category)
        active_category = NoteCategory.objects.get(id=category)
    if author:
        notes = notes.filter(profile__id=author)
        active_author = Profile.objects.get(id=author)
    if order_by:
        notes = notes.order_by(order_by)

    categories = NoteCategory.objects.all()

    p = Paginator(notes, 5)
    page_objects = p.page(page)

    categories = NoteCategory.objects.all()

    # получили избранное
    favorites = None
    if request.user.is_authenticated:
        profile = request.user.profile
        favorites = Favorites.objects.filter(profile=profile)

    context = {
        'notes': notes,
        'categories': categories,
        'active_category': active_category,
        'favorites': favorites,
        'active_author': active_author,
        'page_objects': page_objects
    }

    return render(request, 'notes.html', context)

def notes_search(request):

    notes = Note.objects.all()

    # фильтрация по слову
    text = request.GET.get('text')
    if text:
        notes = notes.filter(Q(title__icontains=text) | Q(text__icontains=text))

    page = request.GET.get('page', 1)
    p = Paginator(notes, 5)
    # page_objects = p.page(page)
    page_objects = p.get_page(page)
    categories = NoteCategory.objects.all()

    context = {
        'page_objects': page_objects,
        'categories': categories,
        'search_text': text,
    }

    return render(request, 'notes.html', context)



def note_detail(request, note_id):
    context = {}

    comment_form = CommentAddForm()
    note = Note.objects.get(id=note_id)
    comments = NoteComment.objects.filter(note=note)

    if request.user.is_authenticated:
        # проверка текущего пользователя на избранное
        in_favorites = Favorites.objects.filter(profile=request.user.profile,
                                                author=note.profile)

        context.update({'in_favorites': in_favorites})

    if request.method == 'POST':
        comment_form = CommentAddForm(request.POST)

        # 2. Достать данные из формы
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']

            profile = request.user.profile
            # 3. Если все ок, то создать комментарий в базе
            NoteComment.objects.create(note=note, text=text, profile=profile)

            # 4. Возвращаемся на страницу
            return redirect('note_detail', note.id)

    context = {
        'note': note,
        'comments': comments,
        'comment_add_form': comment_form
    }

    return render(request, 'note_detail.html', context)


@login_required
def note_add(request):

    categories = NoteCategory.objects.all()
    note_add_form = NoteAddModelForm()

    if request.method == "POST":
        note_add_form = NoteAddModelForm(request.POST)

        if note_add_form.is_valid():
            # data = note_add_form.cleaned_data
            # print(data)
            note = note_add_form.save(commit=False)

            profile = request.user.profile

            note.profile = profile

            note.save()

            # добавили объект в базу
            # Note.objects.create(title=data['title'],
            #                     text=data['text'],
            #                     category=data['category'],
            #                     profile=profile)

            return redirect('notes')

    context = {
        'categories': categories,
        'note_add_form': note_add_form
    }

    return render(request, 'note_add.html', context)


@login_required
def note_edit(request, note_id):
    """Редактирование заметки"""

    note = Note.objects.get(id=note_id)

    # проверка на то, что редактируем свой пост
    if note.profile != request.user.profile:
        raise Http404

    form = NoteAddModelForm(instance=note)

    if request.method == 'POST':
        form = NoteAddModelForm(request.POST, instance=note)
        if form.is_valid():
            # обновление объекта
            form.save()

            return redirect('note_detail', note.id)

    return render(request, 'note_edit.html', {"note_add_form": form})


#Старое представление
# def feedback(request):
#
#     form = FeedbackForm()
#
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#
#         if form.is_valid():
#             data = form.cleaned_data
#
#             Feedback.objects.create(name=data['name'], text=data['text'])
#             return redirect('feedback_success')
#
#     return render(request, 'feedback.html', {'form': form})


def feedback(request):
    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()

            # Feedback.objects.create(name=data['name'], text=data['text'])
            return redirect('feedback_success')

    return render(request, 'feedback.html', {'form': form})


def feedback_success(request):
    return render(request, 'feedback_success.html')


@login_required
def favorites(request, profile_id):

    redirect_url = request.GET.get('next')
    author = Profile.objects.get(id=profile_id)
    profile = request.user.profile

    Favorites.objects.get_or_create(author=author, profile=profile)

    return redirect(redirect_url)

@login_required
def unfavorites(request, profile_id):

    redirect_url = request.GET.get('next')
    author = Profile.objects.get(id=profile_id)
    profile = request.user.profile

    Favorites.objects.filter(author=author, profile=profile).delete()

    return redirect(redirect_url)



# def comment_add(request, note_id):
#
#     if request.method == 'POST':
#         comment_form = CommentAddForm(request.POST)
#
#         # 1. Достать запись из базы по post_id
#         note = Note.objects.get(id=note_id)
#
#         # 2. Достать данные из формы
#         if comment_form.is_valid():
#             text = comment_form.cleaned_data['text']
#
#             # 3. Если все ок, то создать комментарий в базе
#             NoteComment.objects.create(note=note, text=text)
#
#             # 4. Возвращаемся на страницу
#             return redirect('note_detail', note.id)



# def note_add_submit(request):
#
#     # достали данные
#     title = request.POST.get('title')
#     text = request.POST.get('text')
#
#     # добавили объект в базу
#     Note.objects.create(title=title, text=text)
#
#     return redirect('notes')
