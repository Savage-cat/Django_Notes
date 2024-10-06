from django.contrib import admin
from django.urls import path, include

from .views import *
from .classy_views import *

urlpatterns = [
    path('', main, name='main'),

    path('notes', notes, name='notes'),
    path('notes/search', notes_search, name='notes_search'),
    path('notes/<int:note_id>', note_detail, name='note_detail'),
    path('notes/add', note_add, name='note_add'),
    path('notes/<int:note_id>/edit', note_edit, name='note_edit'),

    path('feedback', FeedbackView.as_view(), name='feedback'),
    path('feedback/success', feedback_success, name='feedback_success'),

    path('favorites/<int:profile_id>', favorites, name='favorites'),
    path('unfavorites/<int:profile_id>', unfavorites, name='unfavorites'),

    # path('notes/<int:note_id>/comment/add', comment_add, name='comment_add')
    # path('notes/add_submit', note_add_submit, name='note_add_submit'),
]
