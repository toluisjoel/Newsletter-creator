from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser

from .models import Email
from .serializers import EmailSerializer


class EmailViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [IsAdminUser]
