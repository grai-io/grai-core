import subprocess

from grai_cli.settings.cache import cache


def prep_posthog(posthog):
    posthog.project_api_key = "phc_Q8OCDm0JpCwt4Akk3pMybuBWniWPfOsJzRrdxWjAnjE"
    posthog.host = "https://app.posthog.com"
    posthog.disabled = not cache.telemetry_consent


def capture(event):
    import posthog

    prep_posthog(posthog)
    posthog.capture(cache.telemetry_id, event, groups={"package": "grai-cli"})


class Telemetry:
    @staticmethod
    def capture(event: str):
        subprocess.Popen(["grai", "telemetry", "log", event])
