import uuid

from django.db import models


class BaseModel(models.Model):
    """Базовая абстрактная модель. Добавляет UUID, поля времени создания и обновления по дефолту."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
        db_index=True,
    )
    # При QuerySet.update() поле "updated_at" не обновляется автоматически, нужно обновлять вручную!!!
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Время последнего обновления",
    )

    class Meta:
        abstract = True
