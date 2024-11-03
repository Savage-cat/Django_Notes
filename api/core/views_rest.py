from rest_framework.response import Response
from rest_framework.decorators import api_view
import random

from core.models import NoteComment, Note

from .serializers import CommentsSerializer, NoteSerializer

@api_view(['GET'])
def test_view(request):
    return Response({'message': 'Hello world!'})


@api_view(['GET'])
def comments_list_rest(request, note_id):

    comments = NoteComment.objects.filter(note__id=note_id)

    serializer = CommentsSerializer(comments, many=True)

    return Response({'comments': serializer.data})

@api_view(['POST'])
def comments_add_rest(request, note_id):

    note = Note.objects.get(id=note_id)
    profile = request.user.profile

    serializer = CommentsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save(note=note, profile=profile)

    return Response(status=200)


@api_view(['GET'])
def clicks(request):
    return Response({'clicks': random.randint(1, 100)})

@api_view(['GET'])
def comments(request):

    comments = NoteComment.objects.all()
    serializer = CommentsSerializer(comments, many=True)

    return Response({'comments': serializer.data})


@api_view(['GET'])
def notes(request):

    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)

    return Response({'notes': serializer.data})


@api_view(['POST'])
def film_add_rest(request):

    print(request.data)

    return Response({'film': request.data})
