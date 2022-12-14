import os

from django.http import FileResponse, Http404, HttpResponse
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from src.audio_library.models import Genre, Track, Comment
from src.audio_library.serializers import (
    GenreSerializer,
    LicenseSerializer,
    AlbumSerializer,
    CreateAuthorTrackSerializer,
    AuthorTrackSerializer,
    CreatePlayListSerializer,
    PlayListSerializer,
    CommentSerializer,
    CommentAuthorSerializer,

)
from django.shortcuts import get_object_or_404
from src.base.permissions import IsAuthorOrReadOnly
from src.audio_library.models import License, Album
from rest_framework.parsers import MultiPartParser
from src.base.permissions import IsAuthorOrReadOnly
from src.base.service import delete_old_file
from src.base.classes import Pagination
from django_filters.rest_framework import DjangoFilterBackend


class GenreView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    serializer_class = LicenseSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(isinstance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(user__id=self.kwargs['pk'], private=False)


class TrackView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthorOrReadOnly]


    def get_queryset(self):
        return Track.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorTrackSerializer
        return CreateAuthorTrackSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


class PlayListView(viewsets.ModelViewSet):
    parser_classes = MultiPartParser
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PlayListSerializer
        return CreatePlayListSerializer


class TrackListView(generics.ListAPIView):
    queryset = Track.objects.filter(album__private=False, private=False)
    serializer_class = AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']

class AuthorTrackListView(generics.ListAPIView):
    serializer_class = AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'album__name', 'genre__name']

    def get_queryset(self):
        return Track.objects.filter(
            user__id=self.kwargs['pk'], album__private=False, private=False
        )


class StreamingFileView(APIView):

    def set_play(self, track):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_play()
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"
            return response
        else:
            return Http404


class DownloadTrackView(APIView):

    def set_download(self):
        self.track.dowload += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_download()
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response["Content-Disposition"] = f"attachment; filename={self.track.file.name}"
            response['X-Accel-Redirect'] = f"/media/{self.track.file.name}"
            return response
        else:
            return Http404


class CommentAuthorView(viewsets.ModelViewSet):
    serializer_class = CommentAuthorSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(track__id=self.kwargs['pk'])


class StreamingFileAuthorView(APIView):
    """ Воспроизведение трека автора
    """
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, pk):
        self.track = get_object_or_404(Track, id=pk, user=request.user)
        if os.path.exists(self.track.file.path):
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"
            return response
        else:
            return Http404