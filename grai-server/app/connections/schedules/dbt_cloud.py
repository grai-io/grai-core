from dbtc import dbtCloudClient
from django.conf import settings
from django.urls import reverse

from connections.models import Connection


def save(model: Connection):
    schedule = model.schedules.get("dbt_cloud")
    api_key = model.secrets.get("api_key")

    assert schedule is not None
    assert api_key is not None

    client = dbtCloudClient(api_key=api_key)

    client_url = f"{settings.NGROK_URL}{reverse('connections:dbt-cloud')}"

    payload = {
        "event_types": ["job.run.completed"],
        "name": "Grai Webhook",
        "client_url": client_url,
        "active": True,
        "description": "A webhook for when jobs are completed",
        "job_ids": [int(schedule.get("job_id"))],
    }

    webhook_id = schedule.get("webhook_id")

    if webhook_id:
        account_id = schedule.get("account_id")
        assert account_id is not None

        client.cloud.update_webhook(account_id=account_id, webhook_id=webhook_id, payload=payload)

    else:
        accounts = client.cloud.list_accounts().get("data")
        account_id = accounts[0]["id"]

        response = client.cloud.create_webhook(account_id=account_id, payload=payload)

        webhook = response.get("data")
        assert webhook is not None

        schedule.update(
            {
                "webhook_id": webhook.get("id"),
                "hmac_secret": webhook.get("hmac_secret"),
                "account_id": account_id,
            }
        )
        model.schedules.update({"dbt_cloud": schedule})
