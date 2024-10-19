from django.urls import path

from core.views import feedback
from .views import *

urlpatterns = [
    path('test', test, name='api_test'),
    path('ajax', ajax, name='api_ajax'),

    path('notes/<int:profile_id>/favorites', favorites, name='api_favorites'),
    path('notes/<profile_id>/unfavorites', unfavorites, name='api_unfavorites'),
    path('feedback', feedback, name='api_feedback'),
]
