import time
from abc import ABC, abstractmethod
from enum import Enum


class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = AgentStatus.PENDING
        self.error = None
        self._start_time = None
        self._end_time = None

    def run(self, context: dict) -> dict:
        self.status = AgentStatus.RUNNING
        self._start_time = time.time()
        try:
            result = self.execute(context)
            self.status = AgentStatus.SUCCESS
            return result
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.error = str(e)
            return {}
        finally:
            self._end_time = time.time()

    def report(self) -> dict:
        duration = None
        if self._start_time and self._end_time:
            duration = round(self._end_time - self._start_time, 2)
        return {
            "agent": self.name,
            "status": self.status.value,
            "error": self.error,
            "duration_seconds": duration,
        }

    from abc import abstractmethod

    @abstractmethod
    def execute(self, context: dict) -> dict:
        pass
