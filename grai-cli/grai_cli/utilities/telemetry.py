import multiprocessing as mp
import subprocess
from multiprocessing import Process

import posthog
from grai_cli.settings.cache import cache

posthog.project_api_key = "phc_Q8OCDm0JpCwt4Akk3pMybuBWniWPfOsJzRrdxWjAnjE"
posthog.host = "https://app.posthog.com"
posthog.disabled = not cache.telemetry_consent


def capture(event):
    posthog.capture(cache.telemetry_id, event, groups={"package": "grai-cli"})


# TODO: Can we make this non-blocking? The API is a little slower with telemetry enabled
class Telemetry:
    @staticmethod
    def capture(event: str):
        subprocess.Popen(["grai", "telemetry", "log", event])
