import requests

from django.shortcuts import render 
from rest_framework.decorators import api_view

from src.oauth.serializers import GoogleAuth
from rest_framework.exceptions import AuthenticationFailed
from src.oauth.services.google import check_google_auth
from rest_framework.response import Response
from rest_framework import status
from src.oauth.services.google import check_google_auth
from src.oauth.services.spotify import spotify_auth


def google_login(request):

    return render(request, 'oauth/google_login.html')


def spotify_login(request):

    return render(request, 'oauth/spotify_login.html')

@api_view(["POST"])
def google_auth(request):
    google_data = GoogleAuth(data=request.data)
    if google_data.is_valid():
        token = check_google_auth(google_data.data)
        return Response(token, status=status.HTTP_201_CREATED)
    else:
        return AuthenticationFailed(code=403, detail='Bad data')


@api_view(['GET'])
def spotify_auth(request):
    token = spotify_auth(request.query_params.get('code'))
    return Response(token)
