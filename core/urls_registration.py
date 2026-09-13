from django.urls import path

from . import views_registration

urlpatterns = [
    path('register/', views_registration.register, name='register'),
]
