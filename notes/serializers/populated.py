from jwt_auth.serializers.common import UserSerializer
from .common import NoteSerializer


class PopulatedNoteSerializer(NoteSerializer):
    owner = UserSerializer()
