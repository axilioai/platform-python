from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunRunTimeConfig")


@_attrs_define
class RunRunTimeConfig:
    """
    Attributes:
        is_immediate (bool):
        is_scheduled (bool):
        schedule_timeout_seconds (int):
        schedule_time (str | Unset):
    """

    is_immediate: bool
    is_scheduled: bool
    schedule_timeout_seconds: int
    schedule_time: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        is_immediate = self.is_immediate

        is_scheduled = self.is_scheduled

        schedule_timeout_seconds = self.schedule_timeout_seconds

        schedule_time = self.schedule_time

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "isImmediate": is_immediate,
                "isScheduled": is_scheduled,
                "scheduleTimeoutSeconds": schedule_timeout_seconds,
            }
        )
        if schedule_time is not UNSET:
            field_dict["scheduleTime"] = schedule_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_immediate = d.pop("isImmediate")

        is_scheduled = d.pop("isScheduled")

        schedule_timeout_seconds = d.pop("scheduleTimeoutSeconds")

        schedule_time = d.pop("scheduleTime", UNSET)

        run_run_time_config = cls(
            is_immediate=is_immediate,
            is_scheduled=is_scheduled,
            schedule_timeout_seconds=schedule_timeout_seconds,
            schedule_time=schedule_time,
        )

        return run_run_time_config
