from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


class BaseAgent(ABC):
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.status = AgentStatus.IDLE
        self.result = None
        self.error = None
        self.started_at = None
        self.finished_at = None

    @abstractmethod
    def execute(self, context: dict) -> dict:
        pass

    def run(self, context: dict) -> dict:
        self.status = AgentStatus.RUNNING
        self.started_at = datetime.now()
        try:
            self.result = self.execute(context)
            self.status = AgentStatus.SUCCESS
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.ERROR
            self.result = {"error": str(e)}
        finally:
            self.finished_at = datetime.now()
        return self.result

    def report(self) -> dict:
        duration = None
        if self.started_at and self.finished_at:
            duration = round((self.finished_at - self.started_at).total_seconds(), 2)
        return {
            "agent": self.name,
            "status": self.status.value,
            "duration_seconds": duration,
            "error": self.error,
        }
