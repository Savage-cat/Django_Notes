from django.urls import path

from .views import *

urlpatterns = [
    path('test', test, name='api_test'),
    path('ajax', ajax, name='api_ajax'),
    path('notes/<int:note_id>/favorites', favorites, name='api_favorites'),
    path('notes/<int:note_id>/unfavorites', unfavorites, name='api_unfavorites'),
]
