from django.db import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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


class DurationRankingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        #TODO detect period (week, month, year, all_time) and filter by it
        tasks_summary = Tasks.objects.\
            filter(
                created_by=user,
                is_active=True,
                cycles__created_by=user,
                cycles__dt_end__gte=models.F('cycles__dt_start'),
                cycles__is_active=True
            ).\
            annotate(
                task_name=models.F('name'),
                interval=models.Sum(
                    models.F('cycles__dt_end') - models.F('cycles__dt_start')
                )
            ).\
            values('task_name', 'interval').\
            order_by('-interval')[0:5]
        projects_summary = Projects.objects.\
            filter(
                created_by=user,
                is_active=True,
                tasks__created_by=user,
                tasks__is_active=True,
                tasks__cycles__created_by=user,
                tasks__cycles__dt_end__gte=models.F('tasks__cycles__dt_start'),
                tasks__cycles__is_active=True
            ).\
            annotate(
                project_name=models.F('name'),
                interval=models.Sum(
                    models.F('tasks__cycles__dt_end') -
                    models.F('tasks__cycles__dt_start')
                )
            ).\
            values('project_name', 'interval').\
            order_by('-interval')[0:5]
        data = {
            'projects': {
                'series': [q['interval'].seconds for q in projects_summary],
                'labels': [q['project_name'] for q in projects_summary]
            },
            'tasks': {
                'series': [q['interval'].seconds for q in tasks_summary],
                'labels': [q['task_name'] for q in tasks_summary]
            }
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class OpenTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        #TODO detect period (week, month, year, all_time) and filter by it
        open_tasks = Tasks.objects.\
            filter(
                created_by=user,
                cycles__created_by=user,
                is_active=True,
                cycles__is_active=True,
                cycles__dt_end__isnull=True
            )
        data = [
            {
                'public_id': q['public_id'],
                'name': q['name']
            }
            for q in open_tasks.values()
        ]
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
