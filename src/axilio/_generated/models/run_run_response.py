from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_run_response_run_metadata import RunRunResponseRunMetadata
    from ..models.run_run_response_variables import RunRunResponseVariables


T = TypeVar("T", bound="RunRunResponse")


@_attrs_define
class RunRunResponse:
    """
    Attributes:
        create_date (datetime.datetime):
        id (str):
        status (str):
        trigger (str):
        update_date (datetime.datetime):
        user_id (str):
        workflow_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        cancelled_at (datetime.datetime | Unset):
        completed_at (datetime.datetime | Unset):
        error_message (str | Unset):
        logs (str | Unset):
        phone_id (str | Unset):
        run_metadata (RunRunResponseRunMetadata | Unset):
        schedule_timeout_seconds (int | Unset):
        session_id (str | Unset):
        started_at (datetime.datetime | Unset):
        success (bool | Unset):
        trace_expired_at (datetime.datetime | Unset):
        variables (RunRunResponseVariables | Unset):
        video_url (str | Unset):
    """

    create_date: datetime.datetime
    id: str
    status: str
    trigger: str
    update_date: datetime.datetime
    user_id: str
    workflow_id: str
    schema: str | Unset = UNSET
    cancelled_at: datetime.datetime | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    error_message: str | Unset = UNSET
    logs: str | Unset = UNSET
    phone_id: str | Unset = UNSET
    run_metadata: RunRunResponseRunMetadata | Unset = UNSET
    schedule_timeout_seconds: int | Unset = UNSET
    session_id: str | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    success: bool | Unset = UNSET
    trace_expired_at: datetime.datetime | Unset = UNSET
    variables: RunRunResponseVariables | Unset = UNSET
    video_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        create_date = self.create_date.isoformat()

        id = self.id

        status = self.status

        trigger = self.trigger

        update_date = self.update_date.isoformat()

        user_id = self.user_id

        workflow_id = self.workflow_id

        schema = self.schema

        cancelled_at: str | Unset = UNSET
        if not isinstance(self.cancelled_at, Unset):
            cancelled_at = self.cancelled_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        error_message = self.error_message

        logs = self.logs

        phone_id = self.phone_id

        run_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.run_metadata, Unset):
            run_metadata = self.run_metadata.to_dict()

        schedule_timeout_seconds = self.schedule_timeout_seconds

        session_id = self.session_id

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        success = self.success

        trace_expired_at: str | Unset = UNSET
        if not isinstance(self.trace_expired_at, Unset):
            trace_expired_at = self.trace_expired_at.isoformat()

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        video_url = self.video_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "create_date": create_date,
                "id": id,
                "status": status,
                "trigger": trigger,
                "update_date": update_date,
                "user_id": user_id,
                "workflow_id": workflow_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if cancelled_at is not UNSET:
            field_dict["cancelled_at"] = cancelled_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if logs is not UNSET:
            field_dict["logs"] = logs
        if phone_id is not UNSET:
            field_dict["phone_id"] = phone_id
        if run_metadata is not UNSET:
            field_dict["run_metadata"] = run_metadata
        if schedule_timeout_seconds is not UNSET:
            field_dict["schedule_timeout_seconds"] = schedule_timeout_seconds
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if success is not UNSET:
            field_dict["success"] = success
        if trace_expired_at is not UNSET:
            field_dict["trace_expired_at"] = trace_expired_at
        if variables is not UNSET:
            field_dict["variables"] = variables
        if video_url is not UNSET:
            field_dict["video_url"] = video_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_run_response_run_metadata import RunRunResponseRunMetadata
        from ..models.run_run_response_variables import RunRunResponseVariables

        d = dict(src_dict)
        create_date = datetime.datetime.fromisoformat(d.pop("create_date"))

        id = d.pop("id")

        status = d.pop("status")

        trigger = d.pop("trigger")

        update_date = datetime.datetime.fromisoformat(d.pop("update_date"))

        user_id = d.pop("user_id")

        workflow_id = d.pop("workflow_id")

        schema = d.pop("$schema", UNSET)

        _cancelled_at = d.pop("cancelled_at", UNSET)
        cancelled_at: datetime.datetime | Unset
        if isinstance(_cancelled_at, Unset):
            cancelled_at = UNSET
        else:
            cancelled_at = datetime.datetime.fromisoformat(_cancelled_at)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)

        error_message = d.pop("error_message", UNSET)

        logs = d.pop("logs", UNSET)

        phone_id = d.pop("phone_id", UNSET)

        _run_metadata = d.pop("run_metadata", UNSET)
        run_metadata: RunRunResponseRunMetadata | Unset
        if isinstance(_run_metadata, Unset):
            run_metadata = UNSET
        else:
            run_metadata = RunRunResponseRunMetadata.from_dict(_run_metadata)

        schedule_timeout_seconds = d.pop("schedule_timeout_seconds", UNSET)

        session_id = d.pop("session_id", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = datetime.datetime.fromisoformat(_started_at)

        success = d.pop("success", UNSET)

        _trace_expired_at = d.pop("trace_expired_at", UNSET)
        trace_expired_at: datetime.datetime | Unset
        if isinstance(_trace_expired_at, Unset):
            trace_expired_at = UNSET
        else:
            trace_expired_at = datetime.datetime.fromisoformat(_trace_expired_at)

        _variables = d.pop("variables", UNSET)
        variables: RunRunResponseVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = RunRunResponseVariables.from_dict(_variables)

        video_url = d.pop("video_url", UNSET)

        run_run_response = cls(
            create_date=create_date,
            id=id,
            status=status,
            trigger=trigger,
            update_date=update_date,
            user_id=user_id,
            workflow_id=workflow_id,
            schema=schema,
            cancelled_at=cancelled_at,
            completed_at=completed_at,
            error_message=error_message,
            logs=logs,
            phone_id=phone_id,
            run_metadata=run_metadata,
            schedule_timeout_seconds=schedule_timeout_seconds,
            session_id=session_id,
            started_at=started_at,
            success=success,
            trace_expired_at=trace_expired_at,
            variables=variables,
            video_url=video_url,
        )

        return run_run_response
