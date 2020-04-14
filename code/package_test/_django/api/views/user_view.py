from rest_framework import viewsets, permissions
from api.serializers import UserSerializer
from api.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_time')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kw):
        import pdb;pdb.set_trace()
        print(1)
        super().create(request, *args, **kw)
