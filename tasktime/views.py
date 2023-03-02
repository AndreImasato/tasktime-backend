from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import CyclesSerializer, ProjectsSerializer, TasksSerializer
from .models import Projects, Cycles, Tasks


#TODO creates a custom permission -> IsOwnerPermission
# Create your views here.
class ProjectsView(ModelViewSet):
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'public_id'

    def list(self, request):
        query_set = Projects.objects.filter(
            created_by=request.user,
            is_active=True
        ).all()
        return Response(
            self.serializer_class(
                query_set,
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
