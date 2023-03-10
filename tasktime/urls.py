from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CyclesView, DurationRankingView, OpenTasksView,
                    ProjectsView, TasksView)

router = DefaultRouter()
router.register(r'projects', ProjectsView, 'projects')
router.register(r'tasks', TasksView, 'tasks')
router.register(r'cycles', CyclesView, 'cycles')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'duration-ranking/',
        DurationRankingView.as_view(),
        name="duration_ranking"
    ),
    path(
        'open-tasks/',
        OpenTasksView.as_view(),
        name="open_tasks"
    ),
]
