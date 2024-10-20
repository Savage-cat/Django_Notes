from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.models import NoteComment, Note

from .serializers import CommentsSerializer

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

