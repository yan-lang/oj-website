from rest_framework import viewsets

from account.models import User
from account.serializers import UserSerializer
from rest_framework import mixins

from permissions import IsSelf


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsSelf]
