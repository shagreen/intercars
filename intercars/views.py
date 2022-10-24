from rest_framework import serializers, views
from rest_framework.response import Response


class Healthcheck(views.APIView):
    """Healthcheck endpoint"""
    serializer_class = serializers.Serializer

    def get(self, _request, **_kwargs) -> Response:
        """Endpoint for checking if app is working.

         TODO: Checks database connection and other stuff
        """
        return Response({"healthcheck": True})
