from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Cycles, Projects, Tasks
from .serializers import CyclesSerializer, ProjectsSerializer, TasksSerializer


# Create your views here.
class ProjectsView(ModelViewSet):   # pylint: disable=R0901
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'public_id'

    def get_queryset(self):
        user = self.request.user
        self.queryset = Projects.objects.filter(
            created_by=user,
            is_active=True
        )
        return self.queryset

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
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TasksView(ModelViewSet):  # pylint: disable=R0901
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "public_id"

    def get_queryset(self):
        user = self.request.user
        self.queryset = Tasks.objects.filter(
            created_by=user,
            is_active=True
        )
        return self.queryset

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
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CyclesView(ModelViewSet): # pylint: disable=R0901
    serializer_class = CyclesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "public_id"

    def get_queryset(self):
        user = self.request.user
        self.queryset = Cycles.objects.filter(
            created_by=user,
            is_active=True
        )
        return self.queryset

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
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
