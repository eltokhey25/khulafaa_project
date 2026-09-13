from django.urls import include, path

urlpatterns = [
    path('', include('core.urls_search')),
    path('', include('core.urls_registration')),
    path('', include('core.urls_manage')),
]

