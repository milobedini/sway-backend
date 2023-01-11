from jwt_auth.serializers.populated import PopulatedUserSerializer
from .common import CommentSerializer


class PopulatedCommentSerializer(CommentSerializer):
    owner = PopulatedUserSerializer()
