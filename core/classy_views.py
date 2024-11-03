from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.forms import FeedbackForm, NoteAddModelForm
from core.models import Note, NoteCategory


class ContactView(View):

    def get(self, request):
        return render(request, 'contacts.html')


class SuperContactView(TemplateView):
    template_name = 'contacts.html'


class FeedbackView(CreateView):
    """Представление для добавления обратной связи"""
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = '/feedback/success'


class NoteSearchView(ListView):
    """Представление для страницы с поиском постов"""
    queryset = Note.objects.all()
    template_name = 'posts.html'
    paginate_by = 10
    extra_context = {'categories': NoteCategory.objects.all()}

    def get_queryset(self):
        """Переопределяет метод get_queryset """
        queryset = super().get_queryset()
        text = self.request.GET.get('text')
        if text:
            queryset = queryset.filter(Q(title__icontains=text) | Q(text__icontains=text))

        return queryset

    # def get_context_data(self):
    #     context = super().get_context_data()
    #
    #     text = self.request.GET.get('text')
    #     # получили подписки
    #     subscriptions = None
    #     if self.request.user.is_authenticated:
    #         profile = self.request.user.profile
    #         subscriptions = Subscription.objects.filter(profile=profile)
    #
    #     context.update({
    #         "subscriptions": subscriptions,
    #         "search_text": text
    #     })
    #     return context


class NoteAddView(LoginRequiredMixin, CreateView):
    """Представление для добавления нового поста"""
    form_class = NoteAddModelForm
    template_name = 'note_add.html'

    def post(self, request, *args, **kwargs):
        """Переопределили метод обработки формы"""
        form = self.get_form()
        if form.is_valid():
            note = form.save(commit=False)
            profile = request.user.profile
            note.profile = profile
            note.save()

            return redirect('notes')
        else:
            return self.form_invalid(form)
