from rest_framework import response, status, viewsets

from user.serializers import RegisterSerializer


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
