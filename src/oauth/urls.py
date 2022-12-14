from django.urls import path
from src.oauth.endpoint import views, auth_views
from src.oauth.endpoint.views import UserView, AuthorView, SocialLinkView

urlpatterns = [
    path('me/', UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('google/', auth_views.google_auth ),
    path('', auth_views.google_login),
    path('spotify-login/', auth_views.spotify_login),
    path('spotify-callback/', auth_views.spotify_auth),
    path('author/', AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>/', AuthorView.as_view({'get': 'retrieve'})),
    path('social/', SocialLinkView.as_view({'get': 'list', 'post': 'create'})),
    path('social/<int:pk>/', SocialLinkView.as_view({'put': 'update', 'delete': 'destroy'})),
]

