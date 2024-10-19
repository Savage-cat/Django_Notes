from django.urls import path

from .views import *

urlpatterns = [
    path('test', test, name='api_test'),
    path('ajax', ajax, name='api_ajax'),
    path('notes/<int:profile_id>/favorites', favorites, name='api_favorites'),
    path('notes/<profile_id>/unfavorites', unfavorites, name='api_unfavorites'),
]
