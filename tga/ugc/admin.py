from django.contrib import admin

from .models import StudentLevels
from .models import Students
from .models import ProjectManagers
from .models import PMWorkTime


@admin.register(StudentLevels)
class StudentLevelsAdmin(admin.ModelAdmin):
    list_display = ("level_name",)
    list_edit = ("level_name",)


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
    )
    list_edit = (
        "telegram_id",
        "first_name",
        "last_name",
    )


@admin.register(ProjectManagers)
class ProjectManagersAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
    )
    list_edit = (
        "first_name",
        "last_name",
    )


@admin.register(PMWorkTime)
class PMWorkTimeAdmin(admin.ModelAdmin):
    list_display = (
        "works_from",
        "works_to",
    )
    list_edit = (
        "works_from",
        "works_to",
    )
