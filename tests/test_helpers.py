"""Tests for utils.helpers."""

import pytest
from utils.helpers import generate_id, format_duration, flatten, compute_checksum, chunk_list


class TestGenerateId:
    def test_returns_string(self):
        assert isinstance(generate_id(), str)

    def test_prefix_included(self):
        uid = generate_id("evt")
        assert uid.startswith("evt-")

    def test_unique_ids(self):
        ids = {generate_id() for _ in range(100)}
        assert len(ids) == 100


class TestFormatDuration:
    def test_seconds_only(self):
        assert format_duration(45.0) == "45.0s"

    def test_minutes_and_seconds(self):
        assert format_duration(125.0) == "2m 5s"

    def test_hours_and_minutes(self):
        assert format_duration(3661.0) == "1h 1m"


class TestFlatten:
    def test_already_flat(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_nested(self):
        assert flatten([[1, 2], [3, [4, 5]]]) == [1, 2, 3, 4, 5]

    def test_empty(self):
        assert flatten([]) == []


class TestComputeChecksum:
    def test_deterministic(self):
        assert compute_checksum("hello") == compute_checksum("hello")

    def test_different_inputs(self):
        assert compute_checksum("foo") != compute_checksum("bar")

    def test_length(self):
        assert len(compute_checksum("test")) == 64


class TestChunkList:
    def test_even_split(self):
        assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_uneven_split(self):
        assert chunk_list([1, 2, 3], 2) == [[1, 2], [3]]

    def test_invalid_size(self):
        with pytest.raises(ValueError):
            chunk_list([1, 2], 0)
