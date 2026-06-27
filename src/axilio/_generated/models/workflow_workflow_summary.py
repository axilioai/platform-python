from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="WorkflowWorkflowSummary")


@_attrs_define
class WorkflowWorkflowSummary:
    """
    Attributes:
        create_date (datetime.datetime):
        goal (str):
        id (str):
        last_run_at (datetime.datetime | None):
        name (str):
        ocr_engine (str):
        organization_id (None | str):
        platform (str):
        status (str):
        update_date (datetime.datetime):
        user_id (str):
    """

    create_date: datetime.datetime
    goal: str
    id: str
    last_run_at: datetime.datetime | None
    name: str
    ocr_engine: str
    organization_id: None | str
    platform: str
    status: str
    update_date: datetime.datetime
    user_id: str

    def to_dict(self) -> dict[str, Any]:
        create_date = self.create_date.isoformat()

        goal = self.goal

        id = self.id

        last_run_at: None | str
        if isinstance(self.last_run_at, datetime.datetime):
            last_run_at = self.last_run_at.isoformat()
        else:
            last_run_at = self.last_run_at

        name = self.name

        ocr_engine = self.ocr_engine

        organization_id: None | str
        organization_id = self.organization_id

        platform = self.platform

        status = self.status

        update_date = self.update_date.isoformat()

        user_id = self.user_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "create_date": create_date,
                "goal": goal,
                "id": id,
                "last_run_at": last_run_at,
                "name": name,
                "ocr_engine": ocr_engine,
                "organization_id": organization_id,
                "platform": platform,
                "status": status,
                "update_date": update_date,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        create_date = datetime.datetime.fromisoformat(d.pop("create_date"))

        goal = d.pop("goal")

        id = d.pop("id")

        def _parse_last_run_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_run_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_run_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_run_at = _parse_last_run_at(d.pop("last_run_at"))

        name = d.pop("name")

        ocr_engine = d.pop("ocr_engine")

        def _parse_organization_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        organization_id = _parse_organization_id(d.pop("organization_id"))

        platform = d.pop("platform")

        status = d.pop("status")

        update_date = datetime.datetime.fromisoformat(d.pop("update_date"))

        user_id = d.pop("user_id")

        workflow_workflow_summary = cls(
            create_date=create_date,
            goal=goal,
            id=id,
            last_run_at=last_run_at,
            name=name,
            ocr_engine=ocr_engine,
            organization_id=organization_id,
            platform=platform,
            status=status,
            update_date=update_date,
            user_id=user_id,
        )

        return workflow_workflow_summary
