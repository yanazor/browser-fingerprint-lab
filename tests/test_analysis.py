"""Unit tests for the exploratory analysis helpers."""

from __future__ import annotations

import math

from analysis import entropy, information_gain


def test_entropy_returns_zero_for_empty_input() -> None:
    assert entropy([]) == 0.0


def test_entropy_returns_one_bit_for_balanced_binary_values() -> None:
    result = entropy(["a", "a", "b", "b"])

    assert math.isclose(result, 1.0)


def test_information_gain_detects_perfect_categorical_split() -> None:
    members = ["x", "x", "y", "y"]
    split = ["group-a", "group-a", "group-b", "group-b"]

    result = information_gain(members, split)

    assert math.isclose(result, 1.0)


def test_information_gain_rejects_different_sequence_lengths() -> None:
    assert information_gain(["a"], ["x", "y"]) == 0.0
