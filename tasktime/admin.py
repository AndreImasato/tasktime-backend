from django.contrib import admin
from .models import Projects, Tasks, Cycles


# Register your models here.
@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    pass


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    pass


@admin.register(Cycles)
class CyclesAdmin(admin.ModelAdmin):
    pass
