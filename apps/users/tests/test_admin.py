from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest

from apps.users.admin import UserAdmin
from apps.users.models import User

pytestmark = pytest.mark.django_db


class _AdminRequest(HttpRequest):
    user: User


def _request_for(user: User) -> HttpRequest:
    request = _AdminRequest()
    request.user = user
    return request


def _user_admin() -> UserAdmin:
    return UserAdmin(User, AdminSite())


def test_activate_users() -> None:
    """Экшен активирует выбранных пользователей."""
    user = User.objects.create(username="inactive-user", is_active=False)
    request = _request_for(user)
    action_time = user.updated_at + timedelta(seconds=1)
    user_admin = _user_admin()

    with (
        patch("apps.users.admin.timezone.now", return_value=action_time),
        patch.object(user_admin, "message_user") as message_user,
    ):
        user_admin.activate_users(request, User.objects.filter(pk=user.pk))

    user.refresh_from_db()
    assert user.is_active is True
    assert user.updated_at == action_time
    message_user.assert_called_once_with(request, "Активировано пользователей: 1")


def test_deactivate_users_excludes_current_user() -> None:
    """Экшен блокирует выбранных пользователей, но не текущего."""
    current_user = User.objects.create(username="current-active-user")
    other_user = User.objects.create(username="other-active-user")
    current_updated_at = current_user.updated_at
    request = _request_for(current_user)
    action_time = other_user.updated_at + timedelta(seconds=1)
    user_admin = _user_admin()
    queryset = User.objects.filter(pk__in=(current_user.pk, other_user.pk))

    with (
        patch("apps.users.admin.timezone.now", return_value=action_time),
        patch.object(user_admin, "message_user") as message_user,
    ):
        user_admin.deactivate_users(request, queryset)

    current_user.refresh_from_db()
    other_user.refresh_from_db()
    assert current_user.is_active is True
    assert current_user.updated_at == current_updated_at
    assert other_user.is_active is False
    assert other_user.updated_at == action_time
    message_user.assert_called_once_with(request, "Заблокировано пользователей: 1")


def test_make_staff() -> None:
    """Экшен выдаёт выбранным пользователям статус персонала."""
    user = User.objects.create(username="non-staff-user", is_staff=False)
    request = _request_for(user)
    action_time = user.updated_at + timedelta(seconds=1)
    user_admin = _user_admin()

    with (
        patch("apps.users.admin.timezone.now", return_value=action_time),
        patch.object(user_admin, "message_user") as message_user,
    ):
        user_admin.make_staff(request, User.objects.filter(pk=user.pk))

    user.refresh_from_db()
    assert user.is_staff is True
    assert user.updated_at == action_time
    message_user.assert_called_once_with(request, "Статус персонала выдан: 1")


def test_remove_staff_excludes_current_user() -> None:
    """Экшен снимает статус персонала у выбранных, но не у текущего."""
    current_user = User.objects.create(username="current-staff-user", is_staff=True)
    other_user = User.objects.create(username="other-staff-user", is_staff=True)
    current_updated_at = current_user.updated_at
    request = _request_for(current_user)
    action_time = other_user.updated_at + timedelta(seconds=1)
    user_admin = _user_admin()
    queryset = User.objects.filter(pk__in=(current_user.pk, other_user.pk))

    with (
        patch("apps.users.admin.timezone.now", return_value=action_time),
        patch.object(user_admin, "message_user") as message_user,
    ):
        user_admin.remove_staff(request, queryset)

    current_user.refresh_from_db()
    other_user.refresh_from_db()
    assert current_user.is_staff is True
    assert current_user.updated_at == current_updated_at
    assert other_user.is_staff is False
    assert other_user.updated_at == action_time
    message_user.assert_called_once_with(request, "Статус персонала снят: 1")
