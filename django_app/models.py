from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_permission(value: int):
    if not 1 <= value <= 9:
        raise ValidationError(_("%(value)s должен быть от 1 до 9"), params={"value": value})


class Units(models.Model):
    """
    Номера отделов присваиваются согласно кодам:
    100 (IT):
        110 (разработчики)
        120 (аналитики)
        130 (тестировщики)
    200 (хозяйственная часть)
    300 (администрация):
        310 (бухгалтерия)
        320 (отдел кадров)
    """
    id = models.SmallIntegerField(primary_key=True)
    unitname = models.CharField(max_length=255)

    def __str__(self):
        return self.unitname


class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.username


class Jobs(models.Model):
    jobname = models.CharField(max_length=255, blank=False)

    # Уровни разрешений от самого низкого (1) до самого высокого (9)
    permission = models.SmallIntegerField(validators=[validate_permission])
    unit = models.SmallIntegerField()
    user_jobs = models.ManyToManyField(Users, blank=True)

    def __str__(self):
        return self.jobname
