from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'إدارة نتائج المسابقة'
admin.site.site_title = 'نتائج القرآن'
admin.site.index_title = 'لوحة التحكم'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
