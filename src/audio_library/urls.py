from django.urls import path
from src.audio_library.views import (
    GenreView,
    LicenseView,
    AlbumView,
    PublicAlbumView,
    TrackView,
    PlayListView,
    TrackListView,
    AuthorTrackListView,
    StreamingFileView,
    DownloadTrackView,
    CommentAuthorView,
    CommentView,
    StreamingFileAuthorView
)


urlpatterns = [
    path('genre/', GenreView.as_view()),

    path('license/', LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path('license/<int:pk>/', LicenseView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('album/', AlbumView.as_view({'get': 'list', 'post': 'create'})),
    path('album/<int:pk>/', AlbumView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('author-album/<int:pk>/', PublicAlbumView.as_view()),

    path('track/', TrackView.as_view({'get': 'list', 'post': 'create'})),
    path('track/<int:pk>/', TrackView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('stream-track/<int:pk>/', StreamingFileView.as_view()),
    path('download-track/<int:pk>/', DownloadTrackView.as_view()),

    path('stream-author-track/<int:pk>/', StreamingFileAuthorView.as_view()),

    path('track-list', TrackListView.as_view()),
    path('author-track-list/<int:pk>/', AuthorTrackListView.as_view()),

    path('comments/', CommentAuthorView.as_view({'get': 'list', 'post': 'create'})),
    path('comments/<int:pk>/', CommentAuthorView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('comments_by_track/<int:pk>/', CommentView.as_view({'get': 'list'})),

    path('playlist/', PlayListView.as_view({'get': 'list', 'post': 'create'})),
    path('playlist/<int:pk>/', PlayListView.as_view({'put': 'update', 'delete': 'destroy'})),
]