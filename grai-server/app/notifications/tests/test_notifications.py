import uuid

import pytest

from api.tests.common import test_organisation, test_workspace
from notifications.models import Alert
from notifications.notifications import send_notification


@pytest.mark.django_db
def test_send_notification():
    send_notification("test", "test message")


@pytest.mark.django_db
def test_send_notification_with_alerts(test_workspace):
    Alert.objects.create(
        name=str(uuid.uuid4()),
        workspace=test_workspace,
        channel="email",
        channel_metadata={"emails": []},
        triggers={"test": True},
    )

    send_notification("test", "test message")


@pytest.mark.django_db
def test_send_notification_with_alerts_no_channel(test_workspace):
    Alert.objects.create(
        name=str(uuid.uuid4()),
        workspace=test_workspace,
        channel="test",
        triggers={"test": True},
    )

    with pytest.raises(Exception) as e_info:
        send_notification("test", "test message")

    assert str(e_info.value) == "Notification channel test not supported"
