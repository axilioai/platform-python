from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_inference import UsageInference


T = TypeVar("T", bound="UsageInferencesResponse")


@_attrs_define
class UsageInferencesResponse:
    """
    Attributes:
        inferences (list[UsageInference] | None):
        limit (int):
        offset (int):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    inferences: list[UsageInference] | None
    limit: int
    offset: int
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        inferences: list[dict[str, Any]] | None
        if isinstance(self.inferences, list):
            inferences = []
            for inferences_type_0_item_data in self.inferences:
                inferences_type_0_item = inferences_type_0_item_data.to_dict()
                inferences.append(inferences_type_0_item)

        else:
            inferences = self.inferences

        limit = self.limit

        offset = self.offset

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "inferences": inferences,
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_inference import UsageInference

        d = dict(src_dict)

        def _parse_inferences(data: object) -> list[UsageInference] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                inferences_type_0 = []
                _inferences_type_0 = data
                for inferences_type_0_item_data in _inferences_type_0:
                    inferences_type_0_item = UsageInference.from_dict(inferences_type_0_item_data)

                    inferences_type_0.append(inferences_type_0_item)

                return inferences_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageInference] | None, data)

        inferences = _parse_inferences(d.pop("inferences"))

        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        usage_inferences_response = cls(
            inferences=inferences,
            limit=limit,
            offset=offset,
            total=total,
            schema=schema,
        )

        return usage_inferences_response
