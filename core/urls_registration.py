from django.urls import path

from . import views_registration

urlpatterns = [
    path('register/', views_registration.register, name='register'),
    path(
        'register/history/',
        views_registration.participant_history_search,
        name='participant_history_search',
    ),
    path(
        'register/history/<str:participant_id>/',
        views_registration.participant_history,
        name='participant_history',
    ),
    path(
        'register/success/<str:participant_id>/',
        views_registration.registration_success,
        name='registration_success',
    ),
    path(
        'register/print/<str:participant_id>/',
        views_registration.registration_print,
        name='registration_print',
    ),
]
