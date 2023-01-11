from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers.common import NoteSerializer
from .models import Note
from .serializers.populated import PopulatedNoteSerializer

# Create your views here.


class NoteListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        notes = Note.objects.filter(owner_id=request.user.id)
        serialized_notes = PopulatedNoteSerializer(notes, many=True)
        return Response(serialized_notes.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["owner"] = request.user.id
        note_to_create = NoteSerializer(data=request.data)
        if note_to_create.is_valid():
            note_to_create.save()
            return Response(note_to_create.data, status=status.HTTP_201_CREATED)
        return Response(note_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class NoteDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def delete(self, request, pk):
        try:
            note_to_delete = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise NotFound(detail="Note not found")
        if note_to_delete.owner != request.user:
            raise PermissionDenied()
        note_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        try:
            note_to_update = Note.objects.get(pk=pk)
            request.data["owner"] = request.user.id
        except Note.DoesNotExist:
            raise NotFound(detail="Note not found")
        if note_to_update.owner != request.user:
            raise PermissionDenied()
        serialized_note = NoteSerializer(note_to_update, data=request.data)
        if serialized_note.is_valid():
            serialized_note.save()
            return Response(serialized_note.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serialized_note.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
