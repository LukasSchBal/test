"""Data models for the application."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Event:
    """Represents a process event."""

    event_id: str
    name: str
    timestamp: datetime
    resource: Optional[str] = None
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "name": self.name,
            "timestamp": self.timestamp.isoformat(),
            "resource": self.resource,
            "attributes": self.attributes,
        }


@dataclass
class Case:
    """Represents a process case (trace)."""

    case_id: str
    events: List[Event] = field(default_factory=list)

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    @property
    def duration(self) -> Optional[float]:
        if len(self.events) < 2:
            return None
        start = min(e.timestamp for e in self.events)
        end = max(e.timestamp for e in self.events)
        return (end - start).total_seconds()

    def __len__(self) -> int:
        return len(self.events)


@dataclass
class ProcessLog:
    """Collection of cases forming a process event log."""

    log_id: str
    cases: List[Case] = field(default_factory=list)

    def add_case(self, case: Case) -> None:
        self.cases.append(case)

    @property
    def num_events(self) -> int:
        return sum(len(c) for c in self.cases)

    def get_case(self, case_id: str) -> Optional[Case]:
        for case in self.cases:
            if case.case_id == case_id:
                return case
        return None
