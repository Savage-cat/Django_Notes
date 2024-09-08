
from django.contrib import admin

# Register your models here.

from .models import Note, NoteCategory, NoteComment, Feedback

admin.site.register(Note)
admin.site.register(NoteCategory)
admin.site.register(NoteComment)
admin.site.register(Feedback)


