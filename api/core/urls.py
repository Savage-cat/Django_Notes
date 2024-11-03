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

    path('rest/clicks', clicks, name='clicks'),
    path('rest/comments', comments, name='api_rest_comments'),
    path('rest/notes', notes, name='api_rest_notes'),

    path('rest/film', film_add_rest, name='api_rest_film_add'),
    path('film', film_add, name='film_add'),

]
