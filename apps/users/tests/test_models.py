from datetime import timedelta
from unittest.mock import patch
from uuid import UUID

import pytest

from apps.users.models import User

UUID7_VERSION = 7

pytestmark = pytest.mark.django_db


def test_user_is_created_with_uuid7_primary_key() -> None:
    """Пользователь сохраняется с UUID версии 7 из BaseModel."""
    user = User.objects.create(username="uuid-user")

    assert isinstance(user.pk, UUID)
    assert user.pk.version == UUID7_VERSION
    assert User.objects.filter(pk=user.pk).exists()


def test_updated_at_is_stable_after_create_and_changes_on_save() -> None:
    """После создания updated_at стабилен до следующего вызова save."""
    user = User.objects.create(username="timestamp-user")
    updated_at_after_create = user.updated_at

    user.refresh_from_db()

    assert user.updated_at == updated_at_after_create

    next_updated_at = updated_at_after_create + timedelta(seconds=1)
    with patch("django.db.models.fields.timezone.now", return_value=next_updated_at):
        user.first_name = "Updated"
        user.save()

    assert user.updated_at == next_updated_at
