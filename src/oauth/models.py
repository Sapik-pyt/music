from django.db import models
from django.core.validators import FileExtensionValidator
from src.base.service import get_path_upload_avatar, validate_size_image

class AuthUser(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True)
    display_name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )

    @property
    def is_authentucated(self):
        return True

    def __str__(self):
        return self.email
# Create your models here.


class Follower(models.Model):

    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    subscriber = models.ForeignKey(
        AuthUser, 
        on_delete=models.CASCADE,
        related_name='subscribers'
    )

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'


class SocialLink(models.Model):
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='social_links',   
    )
    link = models.URLField(max_length=100)

    def __str__(self):
        return f'{self.user}'