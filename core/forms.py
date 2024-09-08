from django import forms
from django.core.exceptions import ValidationError

from .models import NoteCategory, Note


class NoteAddForm(forms.Form):
    title = forms.CharField(max_length=500)
    text = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=NoteCategory.objects.all())

    def clean_text(self):
        text = self.cleaned_data['text']
        words = ['дурак', 'козел']
        for word in words:
            if word in text.lower():
                raise ValidationError('Не прошло цензуру')
        return text

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        category = cleaned_data.get("category")

        if Note.objects.filter(title=title, category=category):
            raise ValidationError('В этой категории есть такой пост!')

        return cleaned_data


class NoteAddModelForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'category']


class CommentAddForm(forms.Form):
    text = forms.CharField(max_length=1000, label='Текст')


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Имя')
    text = forms.CharField(label='Текст', widget=forms.Textarea)
