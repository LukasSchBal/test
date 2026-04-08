"""Tests for src.models."""

import pytest
from datetime import datetime, timedelta
from src.models import Event, Case, ProcessLog


def make_event(name: str, offset_hours: int = 0) -> Event:
    return Event(
        event_id=f"evt-{offset_hours}",
        name=name,
        timestamp=datetime(2024, 1, 1, offset_hours),
        resource="Alice",
    )


class TestEvent:
    def test_to_dict_keys(self):
        event = make_event("Start", 0)
        d = event.to_dict()
        assert set(d.keys()) == {"event_id", "name", "timestamp", "resource", "attributes"}

    def test_to_dict_timestamp_is_string(self):
        event = make_event("Start", 1)
        assert isinstance(event.to_dict()["timestamp"], str)


class TestCase:
    def test_add_event_increases_length(self):
        case = Case(case_id="case-001")
        assert len(case) == 0
        case.add_event(make_event("A", 0))
        assert len(case) == 1

    def test_duration_none_for_single_event(self):
        case = Case(case_id="case-002")
        case.add_event(make_event("A", 0))
        assert case.duration is None

    def test_duration_calculated_correctly(self):
        case = Case(case_id="case-003")
        case.add_event(make_event("A", 0))
        case.add_event(make_event("B", 2))
        assert case.duration == pytest.approx(2 * 3600)


class TestProcessLog:
    def test_num_events(self):
        log = ProcessLog(log_id="log-001")
        for i in range(3):
            case = Case(case_id=f"case-{i}")
            case.add_event(make_event("X", i))
            case.add_event(make_event("Y", i + 1))
            log.add_case(case)
        assert log.num_events == 6

    def test_get_case_existing(self):
        log = ProcessLog(log_id="log-002")
        case = Case(case_id="target")
        log.add_case(case)
        assert log.get_case("target") is case

    def test_get_case_missing(self):
        log = ProcessLog(log_id="log-003")
        assert log.get_case("nope") is None
