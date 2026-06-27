from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.send_command_output_body_result import SendCommandOutputBodyResult


T = TypeVar("T", bound="SendCommandOutputBody")


@_attrs_define
class SendCommandOutputBody:
    """
    Attributes:
        command_id (str):
        status (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        error (str | Unset):
        result (SendCommandOutputBodyResult | Unset):
    """

    command_id: str
    status: str
    schema: str | Unset = UNSET
    error: str | Unset = UNSET
    result: SendCommandOutputBodyResult | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        command_id = self.command_id

        status = self.status

        schema = self.schema

        error = self.error

        result: dict[str, Any] | Unset = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "command_id": command_id,
                "status": status,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if error is not UNSET:
            field_dict["error"] = error
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.send_command_output_body_result import SendCommandOutputBodyResult

        d = dict(src_dict)
        command_id = d.pop("command_id")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        error = d.pop("error", UNSET)

        _result = d.pop("result", UNSET)
        result: SendCommandOutputBodyResult | Unset
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = SendCommandOutputBodyResult.from_dict(_result)

        send_command_output_body = cls(
            command_id=command_id,
            status=status,
            schema=schema,
            error=error,
            result=result,
        )

        return send_command_output_body
