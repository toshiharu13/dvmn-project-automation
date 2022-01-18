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
        max_length=256,
        blank=True,
        default="",
        verbose_name="Имя ученика",
    )
    last_name = models.CharField(
        max_length=256,
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
        max_length=256,
        blank=True,
        default="",
        verbose_name="Имя ПМ-а",
    )
    last_name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Фамилия ПМ-а",
    )

    def __str__(self):
        return f"ПМ {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "ПМ"
        verbose_name_plural = "ПМ-ы"


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

    def __str__(self):
        return f"Работает с {self.works_from} по {self.works_to}"

    class Meta:
        verbose_name = "Часы работы ПМ"
        verbose_name_plural = "Часы работы ПМ"
