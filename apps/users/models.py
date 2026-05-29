from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from common.base_model import BaseModel


class User(AbstractUser, BaseModel):
    """Модель пользователя."""

    patronymic = models.CharField("Отчество", max_length=150, blank=True)
    phone = models.CharField("Телефон", max_length=11, blank=True, db_index=True)

    REQUIRED_FIELDS = ()

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserGroup(Group):
    """Proxy-модель групп для отображения в разделе пользователей."""

    class Meta:
        proxy = True
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
