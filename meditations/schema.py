import graphene
from .models import Meditation

from graphene_django.types import DjangoObjectType


class MeditationType(DjangoObjectType):
    class Meta:
        model = Meditation


class Query(graphene.ObjectType):
    all_meditations = graphene.List(MeditationType)

    def resolve_all_meditations(self, _info, **kwargs):
        return Meditation.objects.all()
