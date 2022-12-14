from rest_framework import viewsets, parsers
from src.oauth.serializers import UserSerialzer, AuthorSerialzer, SocialLinkSerializer
from rest_framework.permissions import IsAuthenticated
from src.oauth.models import AuthUser
from src.base.permissions import IsAuthorOrReadOnly


class UserView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser)
    serializer_class = UserSerialzer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):

    queryset = AuthUser.objects.select_related('social_links')
    serializer_class = AuthorSerialzer


class SocialLinkView(viewsets.ModelViewSet):
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return self.request.user.social_links.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
