from rest_framework import viewsets
# from rest_framework import generics as api_views
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# class ArticleListView(api_views.ListAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
