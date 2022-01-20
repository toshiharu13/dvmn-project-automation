from django.db import models


class StudentLevels(models.Model):
    level_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Навык ученика",
    )

    def __str__(self):
        return f"Группа {self.group_name}"

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


class Students(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name="ID пользователя в телеграмме",
        unique=True,
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Имя ученика",
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Фамилия ученика",
    )
    student_level = models.ForeignKey(
        to="ugc.StudentLevels",
        verbose_name="Уровень ученика",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Ученик {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"


class ProjectManagers(models.Model):
    first_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Имя ПМ-а",
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Фамилия ПМ-а",
    )

    def __str__(self):
        return f"ПМ {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "ПМ"
        verbose_name_plural = "ПМ-ы"


class Projects(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Наменование проекта",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Описание проекта",
    )
    start = models.DateField(
        verbose_name="Дата с",
    )
    end = models.DateField(
        verbose_name="Дата по",
    )

    def __str__(self):
        return f"Проект {self.name}"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проект"


class PMWorkTime(models.Model):
    works_from = models.TimeField(
        verbose_name="Работает с",
    )
    works_to = models.TimeField(
        verbose_name="Работает по",
    )
    project_manager = models.ForeignKey(
        to="ugc.ProjectManagers",
        verbose_name="ПМ",
        on_delete=models.PROTECT,
    )
    project = models.ForeignKey(
        to="ugc.Projects",
        verbose_name="Проект",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Работает с {self.works_from} по {self.works_to}"

    class Meta:
        verbose_name = "Часы работы ПМ"
        verbose_name_plural = "Часы работы ПМ"


class StudentsWorkTime(models.Model):
    works_from = models.TimeField(
        verbose_name="Созвон с",
    )
    works_to = models.TimeField(
        verbose_name="Созвон по",
    )
    project = models.ForeignKey(
        to="ugc.Projects",
        verbose_name="Проект",
        on_delete=models.PROTECT,
    )
    student = models.ForeignKey(
        to="ugc.Students",
        verbose_name="Студент",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Созвон с {self.works_from} по {self.works_to}"

    class Meta:
        verbose_name = "Время созвона студента"
        verbose_name_plural = "Время созвона студента"


class Teams(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Намнование команды",
    )
    project_manager = models.ForeignKey(
        to="ugc.ProjectManagers",
        verbose_name="ПМ",
        on_delete=models.PROTECT,
    )
    project = models.ForeignKey(
        to="ugc.Projects",
        verbose_name="Проект",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Команда {self.name}"

    class Meta:
        verbose_name = "Команда проекта"
        verbose_name_plural = "Команды проектов"


class StudentsToCommands(models.Model):
    team = models.ForeignKey(
        to="ugc.Teams",
        verbose_name="Команда",
        on_delete=models.PROTECT,
    )
    student = models.ForeignKey(
        to="ugc.Students",
        verbose_name="Проект",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Команда {self.team.name} для студента {self.student.name}"

    class Meta:
        verbose_name = "Студент в команде"
        verbose_name_plural = "Студенты в команде"
