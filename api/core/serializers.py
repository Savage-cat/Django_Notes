from rest_framework import serializers

from core.models import NoteComment, Note


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=10)
    my_field = serializers.SerializerMethodField(read_only=True)
    profile = serializers.SerializerMethodField()

    def get_my_field(self, obj):
        return 42

    def get_profile(self, obj):
        return obj.profile.user.username

    def create(self, validated_data):
        """Создаем объект комментария в базе """
        text = validated_data['text']
        profile = validated_data['profile']
        note = validated_data['note']

        return NoteComment.objects.create(text=text, note=note, profile=profile)

        # NoteComment.objects.create(**validated_data)


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

