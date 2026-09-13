from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('result/<str:participant_id>/', views.result, name='result'),
]
