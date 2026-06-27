from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunRunStatsResponse")


@_attrs_define
class RunRunStatsResponse:
    """
    Attributes:
        success_rate (float):
        total_runs (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    success_rate: float
    total_runs: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        success_rate = self.success_rate

        total_runs = self.total_runs

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "success_rate": success_rate,
                "total_runs": total_runs,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success_rate = d.pop("success_rate")

        total_runs = d.pop("total_runs")

        schema = d.pop("$schema", UNSET)

        run_run_stats_response = cls(
            success_rate=success_rate,
            total_runs=total_runs,
            schema=schema,
        )

        return run_run_stats_response
