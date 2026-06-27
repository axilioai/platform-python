from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunRunCreateResponse")


@_attrs_define
class RunRunCreateResponse:
    """
    Attributes:
        run_ids (list[str] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    run_ids: list[str] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        run_ids: list[str] | None
        if isinstance(self.run_ids, list):
            run_ids = self.run_ids

        else:
            run_ids = self.run_ids

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "run_ids": run_ids,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_run_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                run_ids_type_0 = cast(list[str], data)

                return run_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        run_ids = _parse_run_ids(d.pop("run_ids"))

        schema = d.pop("$schema", UNSET)

        run_run_create_response = cls(
            run_ids=run_ids,
            schema=schema,
        )

        return run_run_create_response
