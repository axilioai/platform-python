from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageUsageMetricsRequest")


@_attrs_define
class UsageUsageMetricsRequest:
    """
    Attributes:
        end_date (datetime.datetime):
        granularity (str):
        start_date (datetime.datetime):
        timezone (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    end_date: datetime.datetime
    granularity: str
    start_date: datetime.datetime
    timezone: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        end_date = self.end_date.isoformat()

        granularity = self.granularity

        start_date = self.start_date.isoformat()

        timezone = self.timezone

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "end_date": end_date,
                "granularity": granularity,
                "start_date": start_date,
                "timezone": timezone,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end_date = datetime.datetime.fromisoformat(d.pop("end_date"))

        granularity = d.pop("granularity")

        start_date = datetime.datetime.fromisoformat(d.pop("start_date"))

        timezone = d.pop("timezone")

        schema = d.pop("$schema", UNSET)

        usage_usage_metrics_request = cls(
            end_date=end_date,
            granularity=granularity,
            start_date=start_date,
            timezone=timezone,
            schema=schema,
        )

        return usage_usage_metrics_request
