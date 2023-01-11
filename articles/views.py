from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Article
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from articles.serializers.common import ArticleSerializer
from .serializers.populated import PopulatedArticleSerializer
from django.db.models import F
from django.contrib.humanize.templatetags.humanize import naturaltime

# Create your views here.


class ArticleListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        articles = Article.objects.order_by('-created_at').all()
        serialized_articles = PopulatedArticleSerializer(
            articles, many=True)
        return Response(serialized_articles.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["author"] = request.user.id
        post_to_create = ArticleSerializer(data=request.data)
        if post_to_create.is_valid():
            post_to_create.save()
            return Response(post_to_create.data, status=status.HTTP_201_CREATED)
        return Response(post_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ArticleDetailView(APIView):

    def get(self, request, pk):
        article = Article.objects.get(id=pk)
        article.views = F("views") + 1
        article.save(update_fields=["views"])
        updated_article = Article.objects.get(id=pk)
        serialized_article = PopulatedArticleSerializer(updated_article)
        return Response(serialized_article.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            post_to_delete = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise NotFound(detail="Post not found")
        if post_to_delete.author != request.user:
            raise PermissionDenied()
        post_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        post_to_update = Article.objects.get(id=pk)
        request.data["author"] = request.user.id
        if post_to_update.author != request.user:
            raise PermissionDenied()
        edited_post = ArticleSerializer(post_to_update, data=request.data)
        if edited_post.is_valid():
            edited_post.save()
            return Response(edited_post.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(edited_post.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
