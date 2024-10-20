from django.urls import path

from core.views import feedback
from .views import *
from .views_rest import *

urlpatterns = [
    path('test', test, name='api_test'),
    path('ajax', ajax, name='api_ajax'),

    path('notes/<int:profile_id>/favorites', favorites, name='api_favorites'),
    path('notes/<profile_id>/unfavorites', unfavorites, name='api_unfavorites'),
    path('feedback', feedback, name='api_feedback'),

    path('notes/<int:note_id>/comments', note_comments, name='api_note_comments'),

    path('rest', test_view, name='api_rest_test'),
    path('rest/notes/<int:note_id>/comments', comments_list_rest, name='comments_list_rest'),
    path('rest/notes/<int:note_id>/comments/add', comments_add_rest, name='comments_add_rest'),
]
