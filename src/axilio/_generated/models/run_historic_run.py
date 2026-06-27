from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunHistoricRun")


@_attrs_define
class RunHistoricRun:
    """
    Attributes:
        run_id (str):
        status (str):
        trigger (str):
        user_id (str):
        workflow_id (str):
        cancelled_at (str | Unset):
        completed_at (str | Unset):
        created_at (str | Unset):
        error_message (str | Unset):
        org_id (str | Unset):
        phone_id (str | Unset):
        run_metadata (str | Unset):
        started_at (str | Unset):
        success (bool | Unset):
        video_url (str | Unset):
    """

    run_id: str
    status: str
    trigger: str
    user_id: str
    workflow_id: str
    cancelled_at: str | Unset = UNSET
    completed_at: str | Unset = UNSET
    created_at: str | Unset = UNSET
    error_message: str | Unset = UNSET
    org_id: str | Unset = UNSET
    phone_id: str | Unset = UNSET
    run_metadata: str | Unset = UNSET
    started_at: str | Unset = UNSET
    success: bool | Unset = UNSET
    video_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        status = self.status

        trigger = self.trigger

        user_id = self.user_id

        workflow_id = self.workflow_id

        cancelled_at = self.cancelled_at

        completed_at = self.completed_at

        created_at = self.created_at

        error_message = self.error_message

        org_id = self.org_id

        phone_id = self.phone_id

        run_metadata = self.run_metadata

        started_at = self.started_at

        success = self.success

        video_url = self.video_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "run_id": run_id,
                "status": status,
                "trigger": trigger,
                "user_id": user_id,
                "workflow_id": workflow_id,
            }
        )
        if cancelled_at is not UNSET:
            field_dict["cancelled_at"] = cancelled_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if phone_id is not UNSET:
            field_dict["phone_id"] = phone_id
        if run_metadata is not UNSET:
            field_dict["run_metadata"] = run_metadata
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if success is not UNSET:
            field_dict["success"] = success
        if video_url is not UNSET:
            field_dict["video_url"] = video_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_id = d.pop("run_id")

        status = d.pop("status")

        trigger = d.pop("trigger")

        user_id = d.pop("user_id")

        workflow_id = d.pop("workflow_id")

        cancelled_at = d.pop("cancelled_at", UNSET)

        completed_at = d.pop("completed_at", UNSET)

        created_at = d.pop("created_at", UNSET)

        error_message = d.pop("error_message", UNSET)

        org_id = d.pop("org_id", UNSET)

        phone_id = d.pop("phone_id", UNSET)

        run_metadata = d.pop("run_metadata", UNSET)

        started_at = d.pop("started_at", UNSET)

        success = d.pop("success", UNSET)

        video_url = d.pop("video_url", UNSET)

        run_historic_run = cls(
            run_id=run_id,
            status=status,
            trigger=trigger,
            user_id=user_id,
            workflow_id=workflow_id,
            cancelled_at=cancelled_at,
            completed_at=completed_at,
            created_at=created_at,
            error_message=error_message,
            org_id=org_id,
            phone_id=phone_id,
            run_metadata=run_metadata,
            started_at=started_at,
            success=success,
            video_url=video_url,
        )

        return run_historic_run
