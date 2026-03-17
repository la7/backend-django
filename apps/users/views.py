from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .services import UserService
from .serializers import UserSerializer

class UserListCreateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    @extend_schema(responses=UserSerializer(many=True))
    def get(self, request):
        users = self.service.get_all_users()
        return Response(users, status=status.HTTP_200_OK)

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = self.service.create_user(serializer.validated_data)
        return Response(new_user, status=status.HTTP_201_CREATED)

class UserDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    @extend_schema(responses=UserSerializer)
    def get(self, request, pk):
        user = self.service.get_user_by_id(pk)
        return Response(user, status=status.HTTP_200_OK)

    @extend_schema(request=UserSerializer, responses=UserSerializer)
    def put(self, request, pk):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = self.service.update_user(pk, serializer.validated_data)
        return Response(updated_user, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        self.service.delete_user(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)