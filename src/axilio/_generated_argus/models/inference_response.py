from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inference_data import InferenceData


T = TypeVar("T", bound="InferenceResponse")


@_attrs_define
class InferenceResponse:
    """
    Attributes:
        data (InferenceData):
        analyzer_type (str | Unset): Analyzer type used Default: 'all'.
        type_ (str | Unset): Response type Default: 'analyzer_result'.
    """

    data: InferenceData
    analyzer_type: str | Unset = "all"
    type_: str | Unset = "analyzer_result"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        analyzer_type = self.analyzer_type

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if analyzer_type is not UNSET:
            field_dict["analyzer_type"] = analyzer_type
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inference_data import InferenceData

        d = dict(src_dict)
        data = InferenceData.from_dict(d.pop("data"))

        analyzer_type = d.pop("analyzer_type", UNSET)

        type_ = d.pop("type", UNSET)

        inference_response = cls(
            data=data,
            analyzer_type=analyzer_type,
            type_=type_,
        )

        inference_response.additional_properties = d
        return inference_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
