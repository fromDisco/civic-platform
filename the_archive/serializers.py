# import django models/libraries
from django.contrib.auth.models import User

# import DRF models/libraries
from rest_framework import serializers, status
from rest_framework.response import Response

# import project/app stuff
from common.utils import FileUploadField
from common.utils.check_url_status import is_valid_url

from .models import Location, Upload, Comment, Bookmark, Tag, Link

from geolocation.models import Location
from django.contrib.gis.geos import Point as GEOSPoint


CATEGORY = (
    ("document", "Document"),
    ("image", "Image"),
    ("audio", "Audio"),
    ("video", "Video"),
    ("other", "Other"),
)


class UploadSerializer(serializers.ModelSerializer):
    # user is logged in user
    # readonly=True, because upload user is unique
    # PrimaryKeyRelatedField takes user instance
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    location = serializers.CharField(max_length=50)
    zip_code = serializers.IntegerField()
    address = serializers.CharField(max_length=50, required=False)
    link = serializers.CharField(max_length=250)
    # use custom serializer field
    file = FileUploadField()

    class Meta:
        model = Upload
        fields = "__all__"
        # exclude = ["user"]
        ordering = ["created"]

    def create(self, validated_data):
        # breakpoint()
        # Getting the exact location and saving it to a Location object and saving the Upload object
        # Get the city string, zip_code and address from the validated data

        city = validated_data.get("location")
        zip_code = validated_data.get("zip_code")
        address = validated_data.get("address")

        # Look up the coordinates
        latitude, longitude = Location.get_coordinates_from_city(
            f"{address} {zip_code} {city}"
        )

        # Create a GEOSPoint object for the city coordinates
        coordinates = GEOSPoint(latitude, longitude)
        # breakpoint()
        # Create a Location object for the location
        location, _ = Location.objects.get_or_create(
            city=city,
            zip_code=zip_code,
            address=address,
            coordinates=coordinates,
        )
        # Replace the validated_data with the new created Location field
        validated_data["location"] = location

        # Delete zip_code and address from the validated data to create Upload object

        del validated_data["zip_code"]

        if validated_data.get("address"):
            del validated_data["address"]

        # Checking the url validation
        # Get the link data

        link_data = validated_data.get("link")

        print(validated_data)
        print("++++++++++++")
        # breakpoint()
        # Check if the link is valid and save it as a Link object
        valid_link = is_valid_url(link_data)
        if valid_link.status_code == status.HTTP_200_OK:
            link, _ = Link.objects.get_or_create(url=link_data)
            print(link)
            validated_data["link"] = link

        else:
            error_data = {"error": "The URL you entered is not valid."}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        # Create Upload object
        # breakpoint()
        upload_instance = super().create(validated_data)
        upload_instance.zip_code = None
        # upload_instance.address = None
        # upload_instance.link = None
        # Replacing the zip_code and address from the Upload object with None so it won't ask for it later
        # breakpoint()
        print(upload_instance.__class__)

        # upload_instance.save()

        # serializer = self.__class__(instance=upload_instance)

        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return upload_instance
