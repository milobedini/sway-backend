from rest_framework import serializers
from jwt_auth.serializers.common import UserSerializer
from ..models import Meditation


class FavouriteMeditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meditation
        favourited_by = UserSerializer(many=True)
        fields = ('id', 'favourited_by', 'name',
                  'description', 'audio', 'category')
