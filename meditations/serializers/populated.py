from jwt_auth.serializers.common import UserSerializer
from .common import MeditationSerializer


class PopulatedMeditationSerializer(MeditationSerializer):
    favourited_by = UserSerializer(many=True)
