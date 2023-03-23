from abc import ABC, abstractmethod

from notifications.models import Alert


class BaseChannel(ABC):
    @abstractmethod
    def send(self, message: str, alert: Alert):
        return
