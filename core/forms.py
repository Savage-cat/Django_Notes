from django import forms
from django.core.exceptions import ValidationError

from .models import NoteCategory, Note, Feedback


class NoteAddForm(forms.Form):
    title = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"class": "form-control"}))
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

    def __init__(self, *args, **kwargs):
        super(NoteAddModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

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


class CommentAddForm(forms.Form):
    text = forms.CharField(max_length=1000, label='Текст')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'text']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise ValidationError('Введи хотя бы два слова')
        return name








# class FeedbackForm(forms.Form):
#     name = forms.CharField(label='Имя')
#     text = forms.CharField(label='Текст', widget=forms.Textarea)
#
#     def __init__(self, *args, **kwargs):
#         super(FeedbackForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
#
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         if len(name.split()) < 2:
#             raise ValidationError('Введи хотя бы два слова')
#         return name
