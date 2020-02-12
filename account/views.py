from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from account.models import User
from oj.models import Student
from account.serializers import UserSerializer, StudentSerializer
from rest_framework import mixins

from account.permissions import IsSelf, IsOwner


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated, IsSelf]


class StudentViewset(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsOwner, IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
