from django.urls import path

from . import views_manage

urlpatterns = [
    path('manage/login/', views_manage.manage_login, name='manage_login'),
    path('manage/logout/', views_manage.manage_logout, name='manage_logout'),
    path('manage/', views_manage.manage_dashboard, name='manage_dashboard'),
    path('manage/add/', views_manage.manage_add, name='manage_add'),
    path('manage/edit/<int:pk>/', views_manage.manage_edit, name='manage_edit'),
    path('manage/delete/<int:pk>/', views_manage.manage_delete, name='manage_delete'),
]
