from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet
# from .views import ArticleListView


router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('', ArticleListView.as_view(), name='list_articles_api'),
# ]
