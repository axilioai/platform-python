from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.send_command_input_body_params import SendCommandInputBodyParams


T = TypeVar("T", bound="SendCommandInputBody")


@_attrs_define
class SendCommandInputBody:
    """
    Attributes:
        command (str): command type, e.g. OPEN_APP, GET_STATUS
        schema (str | Unset): A URL to the JSON Schema for this object.
        params (SendCommandInputBodyParams | Unset):
    """

    command: str
    schema: str | Unset = UNSET
    params: SendCommandInputBodyParams | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        schema = self.schema

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "command": command,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.send_command_input_body_params import SendCommandInputBodyParams

        d = dict(src_dict)
        command = d.pop("command")

        schema = d.pop("$schema", UNSET)

        _params = d.pop("params", UNSET)
        params: SendCommandInputBodyParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = SendCommandInputBodyParams.from_dict(_params)

        send_command_input_body = cls(
            command=command,
            schema=schema,
            params=params,
        )

        return send_command_input_body
