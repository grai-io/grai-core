from auth.password_reset import password_reset_generator
from users.models import User, AuditEvents, Audit
from datetime import datetime
import pytest
from uuid import uuid4

TIMESTAMP = datetime.now().replace(microsecond=0, tzinfo=None)


@pytest.mark.django_db
@pytest.fixture
def user():
    user = User(username=f"null@grai.io")
    user.save()
    return user


@pytest.mark.django_db
@pytest.fixture
def audit(user):
    audit = Audit(user_id=user.id, event=AuditEvents.PASSWORD_RESET.name)
    audit.save()
    return audit


@pytest.mark.django_db
@pytest.mark.xfail
def test_pw_reset_hash_no_pw_reset():
    password_reset_generator._make_hash_value(User(username=f"test@grai.io"), TIMESTAMP)


@pytest.mark.django_db
def test_pw_reset_hash(user, audit):
    hash_str = password_reset_generator._make_hash_value(user, TIMESTAMP)
    pk, pw, ts, r_ts, email = hash_str.split("::")

    assert pk == str(user.pk)
    assert pw == user.password
    assert ts == str(TIMESTAMP)
    assert r_ts == str(audit.created_at.replace(microsecond=0, tzinfo=None))
    assert email == user.username
