from django.contrib import admin
from django.urls import path, include
from .data_scrap_api.views import article_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dataScrap.data_scrap_api.urls')),
    path('', article_list_view, name='article_list_view'),
]
