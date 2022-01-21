from django.contrib import admin

from .models import StudentLevels
from .models import Students
from .models import ProjectManagers
from .models import PMWorkTime
from .models import Projects
from .models import StudentsWorkTime
from .models import Teams
from .models import StudentsToCommands


@admin.register(StudentLevels)
class StudentLevelsAdmin(admin.ModelAdmin):
    list_display = ("level_name",)
    list_edit = ("level_name",)


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "student_level",
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
        "project_manager",
        "works_from",
        "works_to",
    )
    list_edit = (
        "works_from",
        "works_to",
    )


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start",
        "end",
    )
    list_edit = (
        "name",
        "start",
        "end",
    )


@admin.register(StudentsWorkTime)
class StudentsWorkTimeAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "student",
        "works_from",
        "works_to",
    )


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "project_manager",
    )


@admin.register(StudentsToCommands)
class StudentsToCommandsAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "student",
    )
