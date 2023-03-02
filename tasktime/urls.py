from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CyclesView, ProjectsView, TasksView

router = DefaultRouter()
router.register(r'projects', ProjectsView, 'projects')
router.register(r'tasks', TasksView, 'tasks')
router.register(r'cycles', CyclesView, 'cycles')

urlpatterns = [
    path('', include(router.urls)),
]
