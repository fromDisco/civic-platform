# import django models/libraries
from django.contrib.auth.models import User

# import DRF models/libraries
from rest_framework import serializers

# import project/app stuff
from common.utils import FileUploadField, FileValidator
from .models import Location, Upload, Comment, Bookmark, Tag, Link

CATEGORY = (
    ("document", "Document"),
    ("image", "Image"),
    ("audio", "Audio"),
    ("video", "Video"),
    ("other", "Other"),
)


class UploadPostSerializer(serializers.ModelSerializer):
    # user is logged-in user
    # readonly=True, because upload user is unique
    # PrimaryKeyRelatedField takes user instance
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # use custom serializer field
    file = FileUploadField(validators=[FileValidator()])

    class Meta:
        model = Upload
        fields = "__all__"
        # exclude = ["user"]
        ordering = ["created"]


class UploadSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Upload
        fields = "__all__"
        ordering = ["created"]