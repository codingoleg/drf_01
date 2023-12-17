from django.db import models


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
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Users(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Jobs(models.Model):
    name = models.CharField(max_length=255, blank=False)

    # Уровни разрешений от самого низкого (1) до самого высокого (9)
    permission = models.SmallIntegerField()
    unit = models.SmallIntegerField()
    user_jobs = models.ManyToManyField(Users, blank=True)

    def __str__(self):
        return self.name
