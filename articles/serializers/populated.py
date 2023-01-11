from .common import ArticleSerializer
from comments.serializers.populated import PopulatedCommentSerializer
from jwt_auth.serializers.populated import PopulatedUserSerializer


class PopulatedArticleSerializer(ArticleSerializer):
    comments = PopulatedCommentSerializer(many=True)
    author = PopulatedUserSerializer()
