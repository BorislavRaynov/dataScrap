from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Article
from .serializers import ArticleSerializer
from .filters import ArticleFilterSet


def article_list_view(request):
    return render(request, 'index.html')


class ArticlePagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('uid')
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_set_class = ArticleFilterSet
    search_fields = ['title', 'body']

    @action(detail=False, methods=['get'], url_path='last')
    def get_last_article(self, request):
        try:
            last_article = Article.objects.latest('uid')
            serializer = self.get_serializer(last_article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response({"detail": "No articles found."}, status=404)

    @action(detail=False, methods=['get'], url_path='recent')
    def get_recent_articles(self, request):
        recent_articles = Article.objects.order_by('-publication_date')[:5]
        serializer = self.get_serializer(recent_articles, many=True)
        return Response(serializer.data)
