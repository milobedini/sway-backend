from .common import UserSerializer
from meditations.serializers.common import MeditationSerializer


class PopulatedUserSerializer(UserSerializer):
    favourites = MeditationSerializer(many=True)
