from rest_framework.serializers import ModelSerializer, IntegerField
from src.audio_library.models import (
    Genre,
    License,
    Album,
    Track,
    PlayList,
    Comment
)
from src.base.service import delete_old_file
from src.oauth.serializers import AuthorSerialzer

class BaseSerializer(ModelSerializer):
    id = IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)


class LicenseSerializer(BaseSerializer):
    class Meta:
        model = License
        fields = ('id', 'text',)


class AlbumSerializer(BaseSerializer):
    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'cover', 'private')

        def update(self, instance, validated_data):
           delete_old_file(instance.cover.path)
           return super().update(instance, validated_data) 


class CreateAuthorTrackSerializer(BaseSerializer):
    plays_count = IntegerField(read_only=True)
    dowload = IntegerField(read_only=True)
    
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['user']

class AuthorTrackSerializer(CreateAuthorTrackSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    user = AuthorSerialzer()


class CreatePlayListSerializer(BaseSerializer):
    
    class Meta:
        model = PlayList
        fields = '__all__'

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    tracks = AuthorTrackSerializer(many=True, read_only=True)


class CommentAuthorSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'track',)


class CommentSerializer(ModelSerializer):
    user = AuthorSerialzer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user', 'track', 'create_at',)
