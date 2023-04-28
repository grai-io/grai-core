import pytest
from notifications.models import Alert

from notifications.notifications import send_notification
from workspaces.models import Organisation, Workspace


@pytest.fixture
def test_organisation():
    return Organisation.objects.create(name="Org1")


@pytest.fixture
def test_workspace(test_organisation):
    return Workspace.objects.create(name="W10", organisation=test_organisation)


@pytest.mark.django_db
def test_send_notification():
    send_notification("test", "test message")


@pytest.mark.django_db
def test_send_notification_with_alerts(test_workspace):
    Alert.objects.create(
        workspace=test_workspace,
        channel="email",
        channel_metadata={"emails": []},
        triggers={"test": True},
    )

    send_notification("test", "test message")


@pytest.mark.django_db
def test_send_notification_with_alerts_no_channel(test_workspace):
    Alert.objects.create(
        workspace=test_workspace,
        channel="test",
        triggers={"test": True},
    )

    with pytest.raises(Exception) as e_info:
        send_notification("test", "test message")

    assert str(e_info.value) == "Notification channel test not supported"
