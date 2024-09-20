from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, NoteCategory, NoteComment, Feedback
from .forms import NoteAddForm, CommentAddForm, FeedbackForm, NoteAddModelForm

def main(request):

    note = Note.objects.all()[0]

    return render(request, 'main.html', {"note": note})


def notes(request):

    notes = Note.objects.all()

    category = request.GET.get('category')
    active_category = None

    if category:
        # достаем посты и фильтруем
        notes = notes.filter(category__id=int(category))
        active_category = NoteCategory.objects.get(id=category)

    categories = NoteCategory.objects.all()

    context = {
        'notes': notes,
        'categories': categories,
        'active_category': active_category
    }

    return render(request, 'notes.html', context)


def note_detail(request, note_id):

    comment_form = CommentAddForm()
    note = Note.objects.get(id=note_id)
    comments = NoteComment.objects.filter(note=note)

    if request.method == 'POST':
        comment_form = CommentAddForm(request.POST)

        # 2. Достать данные из формы
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']

            # 3. Если все ок, то создать комментарий в базе
            NoteComment.objects.create(note=note, text=text)

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
            data = note_add_form.cleaned_data
            print(data)

            profile = request.user.profile
            # добавили объект в базу
            Note.objects.create(title=data['title'],
                                text=data['text'],
                                category=data['category'],
                                profile=profile)

            return redirect('notes')

    context = {
        'categories': categories,
        'note_add_form': note_add_form
    }

    return render(request, 'note_add.html', context)


def feedback(request):

    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            Feedback.objects.create(name=data['name'], text=data['text'])
            return redirect('feedback_success')

    return render(request, 'feedback.html', {'form': form})


def feedback_success(request):
    return render(request, 'feedback_success.html')




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
