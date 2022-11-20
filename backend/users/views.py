from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.views import UserViewSet

class Logout(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
