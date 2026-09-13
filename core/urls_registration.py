from django.urls import path

from . import views_registration

urlpatterns = [
    path('register/', views_registration.register, name='register'),
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
