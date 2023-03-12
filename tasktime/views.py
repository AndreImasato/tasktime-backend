from datetime import date

from django.db import models
from django.db.models.fields import DateField
from django.db.models.functions import (Cast, ExtractMonth, ExtractWeek,
                                        ExtractYear)
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
            ).\
            annotate(
                project_public_id=models.F(
                    'project_id__public_id'
                )
            ).\
            values('public_id', 'name', 'project_public_id')
        data = [
            {
                'public_id': q['public_id'],
                'name': q['name'],
                'project_public_id': q['project_public_id']
            }
            for q in open_tasks
        ]
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class LastModifiedTasks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        latest_tasks = Tasks.objects.\
            filter(
                created_by=user,
                cycles__created_by=user,
                is_active=True,
                cycles__is_active=True,
            ).\
            annotate(
                project_public_id=models.F(
                    'project_id__public_id'
                ),
                last_modified_on=models.F(
                    'cycles__modified_on'
                )
            ).\
            values(
                'public_id',
                'name',
                'project_public_id',
                'last_modified_on'
            ).\
            order_by('-last_modified_on')[0:5]
        data = [
            {
                'public_id': q['public_id'],
                'name': q['name'],
                'project_public_id': q['project_public_id'],
                'last_modified_on': q['last_modified_on']
            }
            for q in latest_tasks
        ]
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class HistogramView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #TODO detect period
        user = request.user
        cycle_base_query = Cycles.objects.\
            filter(
                dt_start__isnull=False,
                created_by=user,
                is_active=True,
                dt_end__gte=models.F('dt_start')
            )
        #TODO change for input date in querystring parameters
        #TODO more flexibility for testing
        current_date = date.today()
        current_week = current_date.isocalendar()[1]
        current_month = current_date.month
        current_year = current_date.year

        # Week
        #TODO convert to the desired timezone
        week_query = cycle_base_query.\
            filter(
                dt_start__week=current_week,
                dt_start__year=current_year
            ).\
            annotate(day=Cast('dt_start', DateField())).\
            values('day').\
            annotate(
                interval=models.Sum(
                    models.F('dt_end') -
                    models.F('dt_start')
                )
            ).\
            values('day', 'interval')
        # Month
        #TODO convert to the desired timezone
        month_query = cycle_base_query.\
            filter(
                dt_start__month=current_month,
                dt_start__year=current_year
            ).\
            annotate(
                day=Cast('dt_start', DateField())
            ).\
            values('day').\
            annotate(
                interval=models.Sum(
                    models.F('dt_end') -
                    models.F('dt_start')
                )
            ).\
            values('day', 'interval')
        # Year
        #TODO convert to the desired timezone
        year_query = cycle_base_query.\
            filter(
                dt_start__year=current_year
            ).\
            annotate(
                month=ExtractMonth('dt_start')
            ).\
            values('month').\
            annotate(
                interval=models.Sum(
                    models.F('dt_end') -
                    models.F('dt_start')
                )
            ).\
            values('month', 'interval')
        #TODO deal when it is the first week of the year
        #TODO convert to the desired timezone
        last_week_query = cycle_base_query.\
            filter(
                dt_start__week=current_week - 1,
                dt_start__year=current_year
            ).\
            aggregate(last_week_interval=models.Sum(
                models.F('dt_end') -
                models.F('dt_start')
            ))
        #TODO deal when it is the first month of the year
        #TODO convert to the desired timezone
        last_month_query = cycle_base_query.\
            filter(
                dt_start__month=current_month - 1,
                dt_start__year=current_year
            ).\
            aggregate(
                last_month_interval=models.Sum(
                    models.F('dt_end') -
                    models.F('dt_start')
                )
            )
        last_year_query = cycle_base_query.\
            filter(
                dt_start__year=current_year - 1
            ).\
            aggregate(
                last_year_interval=models.Sum(
                    models.F('dt_end') -
                    models.F('dt_start')
                )
            )

        data = {
            'week': {
                'plot_data': {
                    'series': [q['interval'].seconds for q in week_query],
                    'xaxis': [q['day'] for q in week_query]
                },
                'additional_info': {
                    'last_value': last_week_query['last_week_interval']
                },
            },
            'month': {
                'plot_data': {
                    'series': [q['interval'].seconds for q in month_query],
                    'xaxis': [q['day'] for q in month_query]
                },
                'additional_info': {
                    'last_value': last_month_query['last_month_interval']
                }
            },
            'year': {
                'plot_data': {
                    'series': [q['interval'].seconds for q in year_query],
                    'xaxis': [q['month'] for q in year_query]
                },
                'additional_info': {
                    'last_value': last_year_query['last_year_interval']
                }
            }
        }

        print(data)

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
