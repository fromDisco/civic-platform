import os
import magic

# import django models/libraries
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse

# import DRF models/libraries
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

# import app models
from .models import Upload, Location, Link, Comment
from .serializers import UploadSerializer, UploadPostSerializer, CommentPostSerializer, CommentSerializer
from common.utils import write_file

# import for TokenAuthentication
# from rest_framework.authentication import TokenAuthentication
# from .permission import IsAdminOrReadOnly


# set limits for number of response elements
class PaginatedProducts(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100  # maximum size of the page that can be set by the API client


class UploadListAPI(ListAPIView):
    # in models.py we defined a custom model manager:
    # upload objects -> UploadObjects()
    # so its possible to only list elements that have "status=published"
    queryset = Upload.uploadobjects.all()
    # queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    # permission_classes = [IsAdminOrReadOnly, ]


class UploadAPI(CreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadPostSerializer
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UploadPostSerializer(data=request.data)

        if serializer.is_valid():
            # read logged in user and set as upload__user:
            # can't be changed afterwards > readonly=True
            serializer.validated_data.update({"user": request.user})

            file_path, category = write_file(request.FILES.get("file"))
            serializer.validated_data.update({"file": file_path})
            serializer.validated_data.update({"media_type": category})
            instance = serializer.save()

            # UploadPostSerializer is only for input
            # for Response create instance of UpolaodSerialzer instead
            serialized_instance = UploadSerializer(instance)

            return Response(serialized_instance.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadModifyApi(GenericAPIView):
    """
    Read, update and delete single db entries
    """
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    warnings = {
        "user_locked": {"warning": "Its not possible to change the upload user."},
    }

    def get(self, request, pk, format=None):
        upload_instance = get_object_or_404(Upload, pk=pk)
        serializer = UploadSerializer(upload_instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        upload_instance = get_object_or_404(Upload, pk=pk)

        # TODO: if-statement and serializer instance are repeated in self.patch
        if request.data.get("user") != upload_instance.user.id:
            return Response(
                self.warnings.get("user_locked"), status=status.HTTP_400_BAD_REQUEST
            )

        # pass the upload instance and the changed values to serializer
        serializer = UploadSerializer(
            instance=upload_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        Use patch instead of put. Using patch doesn't require fields.
        Only changed values have to be passed.
        """
        upload_instance = get_object_or_404(Upload, pk=pk)
        # check if request tries to change unmodifiable upload user
        if (
            request.data.get("user")
            and request.data.get("user") != upload_instance.user.id
        ):
            return Response(
                self.warnings.get("user_locked"), status=status.HTTP_400_BAD_REQUEST
            )

        # pass the upload instance and the changed values to serializer
        serializer = UploadSerializer(
            instance=upload_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        upload_instance = get_object_or_404(Upload, pk=pk)

        try:
            #os.remove(upload_instance.file)
            upload_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UploadDownload(GenericAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    def get(self, request, pk):
        upload_instance = Upload.objects.get(pk=pk)
        upload_file = open(upload_instance.file, "rb")

        mime = magic.Magic(mime=True)
        py_magic = mime.from_file(upload_instance.file)

        filename = os.path.basename(upload_instance.file)

        response = FileResponse(upload_file, content_type=f"{py_magic}")
        response['Content-Length'] = f"{os.path.getsize(upload_instance.file)}"
        response['Content-Disposition'] = f"attachment; filename={filename}"

        return response
    

class CommentCreateApi(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CommentPostSerializer(data=request.data)

        if serializer.is_valid():
            # read logged in user and set as upload__user:
            # can't be changed afterwards > readonly=True
            upload_id = request.data.get("upload")
            upload_instance = Upload.objects.get(pk=upload_id)
            serializer.validated_data.update({"upload": upload_instance})
            serializer.validated_data.update({"author": request.user})

            instance = serializer.save()

            # UploadPostSerializer is only for input
            # for Response create instance of UpolaodSerialzer instead
            serialized_instance = CommentSerializer(instance)

            return Response(serialized_instance.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    pass