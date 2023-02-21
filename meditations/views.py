from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import F, Q


from .models import Meditation
from .serializers.populated import PopulatedMeditationSerializer
from .serializers.favourite import FavouriteMeditationSerializer

# Create your views here.


class MeditationListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        meditations = Meditation.objects.order_by('-created_at').all()

        serialized_meditations = PopulatedMeditationSerializer(
            meditations, many=True)
        return Response(serialized_meditations.data, status=status.HTTP_200_OK)


class MeditationSearchView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        query = request.GET.get('q')
        print(query)
        if not query:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        meditations = Meditation.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        ).order_by('-created_at')

        serialized_meditations = PopulatedMeditationSerializer(
            meditations, many=True)
        return Response(serialized_meditations.data, status=status.HTTP_200_OK)


class MeditationDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        meditation = Meditation.objects.get(id=pk)
        meditation.views = F("views") + 1
        meditation.save(update_fields=["views"])
        updated_meditation = Meditation.objects.get(id=pk)
        serialized_meditation = PopulatedMeditationSerializer(
            updated_meditation)
        return Response(serialized_meditation.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            med_to_fav = Meditation.objects.get(pk=pk)
            print(request.data)
        except Meditation.DoesNotExist:
            raise NotFound(detail="Meditation not found")

        current_user = request.user
        # print(current_user.id)
        if current_user in med_to_fav.favourited_by.all():
            med_to_fav.favourited_by.remove(current_user.id)
            print("UNLIKING")
            return Response(status=status.HTTP_201_CREATED)
        med_to_fav.favourited_by.add(current_user.id)
        print("LIKING")
        med_to_fav.save()
        return Response(status=status.HTTP_201_CREATED)


class LatestMeditationView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        sorted_meditations = Meditation.objects.order_by('-created_at').all()
        meditation = sorted_meditations.first()
        serialized_meditation = PopulatedMeditationSerializer(meditation)
        return Response(serialized_meditation.data, status=status.HTTP_200_OK)
