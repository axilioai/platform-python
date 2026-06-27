from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsageChartDataPoint")


@_attrs_define
class UsageChartDataPoint:
    """
    Attributes:
        is_current (bool):
        period (str):
        timestamp (datetime.datetime):
        value (float):
    """

    is_current: bool
    period: str
    timestamp: datetime.datetime
    value: float

    def to_dict(self) -> dict[str, Any]:
        is_current = self.is_current

        period = self.period

        timestamp = self.timestamp.isoformat()

        value = self.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "is_current": is_current,
                "period": period,
                "timestamp": timestamp,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_current = d.pop("is_current")

        period = d.pop("period")

        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        value = d.pop("value")

        usage_chart_data_point = cls(
            is_current=is_current,
            period=period,
            timestamp=timestamp,
            value=value,
        )

        return usage_chart_data_point
