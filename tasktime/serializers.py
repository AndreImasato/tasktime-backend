from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Cycles, Projects, Tasks

User = get_user_model()


class CyclesSerializer(serializers.ModelSerializer):
    duration = serializers.FloatField(
        read_only=True
    )
    parsed_duration = serializers.CharField(
        read_only=True
    )
    is_active = serializers.BooleanField(
        default=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    def validate(self, attrs):
        if self.partial:
            dt_start = attrs.get('dt_start') or self.instance.dt_start
        else:
            dt_start = attrs.get('dt_start')
        dt_end = attrs.get('dt_end')
        if dt_end is not None:
            if dt_end < dt_start:
                raise serializers.ValidationError(
                    _("Invalid End datetime: end datetime must not be lesser than start datetime"),
                    code="invalid_end_datetime"
                )
            return attrs
        return super().validate(attrs)

    class Meta:
        model = Cycles
        exclude = (
            "id",
        )
        extra_kwargs = {
            "public_id": {"read_only": True},
            "duration": {"read_only": True},
            "parsed_duration": {"read_only": True}
        }


class TasksSerializer(serializers.ModelSerializer):
    duration = serializers.FloatField(
        read_only=True
    )
    parsed_duration = serializers.CharField(
        read_only=True
    )
    cycles = CyclesSerializer(
        many=True,
        read_only=True
    )
    is_active = serializers.BooleanField(
        default=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Tasks
        exclude = (
            "id",
        )
        extra_kwargs = {
            "public_id": {"read_only": True},
            "duration": {"read_only": True},
            "parsed_duration": {"read_only": True}
        }


class ProjectsSerializer(serializers.ModelSerializer):
    duration = serializers.FloatField(
        read_only=True
    )
    parsed_duration = serializers.CharField(
        read_only=True
    )
    tasks = TasksSerializer(
        many=True,
        read_only=True
    )
    is_active = serializers.BooleanField(
        default=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Projects
        exclude = (
            "id",
        )
        extra_kwargs = {
            "public_id": {"read_only": True},
            "duration": {"read_only": True},
            "parsed_duration": {"read_only": True},
        }
