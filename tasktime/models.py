# pylint: disable=C0209
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import CustomUserLogBaseModel
from common.utils import Utils


# Create your models here.
class Projects(CustomUserLogBaseModel):
    name = models.CharField(
        unique=True,
        max_length=50,
        blank=False,
        null=False,
        help_text=_("Project name")
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Project description")
    )

    @property
    def duration(self):
        return sum(
            tk.duration
            for tk in
            self.tasks.all()
        )

    @property
    def parsed_duration(self):
        return Utils.parse_interval(self.duration)

    def __str__(self):
        return "{id} - {name}".format(
            id=self.pk,
            name=self.name
        )

    class Meta:
        db_table = "tasktime_projects"


class Tasks(CustomUserLogBaseModel):
    name = models.CharField(
        unique=True,
        max_length=100,
        blank=False,
        null=False,
        help_text=_("Task name")
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Task description")
    )
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE,
        related_name="tasks",
        related_query_name="tasks",
        help_text=_("Project to which this task is related")
    )

    @property
    def duration(self):
        """
        Total duration for task related cycles
        in seconds
        """
        return sum(
            cy.duration
            for cy in self.cycles.filter(
                dt_end__isnull=False,
                dt_end__gte=models.F('dt_start')
            ).all()
        )

    @property
    def parsed_duration(self):
        """
        Total Duration in format 00:00:00
        """
        return Utils.parse_interval(self.duration)

    def __str__(self):
        return "{id} - {name}".format(
            id=self.pk,
            name=self.name
        )

    class Meta:
        db_table = "tasktime_tasks"


class Cycles(CustomUserLogBaseModel):
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name="cycles",
        related_query_name="cycles",
        help_text=_("Task to which this cycle is related")
    )
    dt_start = models.DateTimeField(
        null=False,
        help_text=_("Start datetime for this cycle")
    )
    dt_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("End datetime for this cycle")
    )

    @property
    def duration(self):
        """
        Duration in seconds
        """
        # Verifies whether end datetime is none or not
        if self.dt_end is None:
            return 0
        if self.dt_start > self.dt_end:
            raise ValueError(
                "Start datetime is greater than corresponding end datetime"
            )
        interval = self.dt_end - self.dt_start
        return int(interval.total_seconds())

    @property
    def parsed_duration(self):
        """
        Duration in format 00:00:00
        """
        return Utils.parse_interval(self.duration)

    class Meta:
        db_table = "tasktime_cycles"
