from rest_framework import serializers
from src.oauth.models import AuthUser, SocialLink

class UserSerialzer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ('avatar', 'county', 'city', 'bio', 'display_name')


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ('link',)


class AuthorSerialzer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True)
    class Meta:
        model = AuthUser
        fields = ('id', 'avatar', 'county', 'city', 'bio', 'display_name', 'social_links')




class GoogleAuth(serializers.Serializer):

    email = serializers.EmailField()
    token = serializers.CharField()