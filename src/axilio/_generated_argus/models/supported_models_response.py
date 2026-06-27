from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_info import ModelInfo


T = TypeVar("T", bound="SupportedModelsResponse")


@_attrs_define
class SupportedModelsResponse:
    """Response for GET /inference/models.

    Lists the VLM models supported for the element-locator task, each with
    its context window and final per-token pricing, so a client can compare
    cost and validate `find(model=...)` up front instead of round-tripping
    to /locate and getting a 400.

    The set is curated: these are the vision-capable models supported for UI
    grounding. `/locate` enforces it — an unsupported model is rejected, so
    this is the authoritative allowlist, not just advisory.

    Shaped like a standard /v1/models response ({object: "list", data: [...]}).

        Attributes:
            data (list[ModelInfo]): Supported models, sorted by id.
            object_ (Literal['list'] | Unset):  Default: 'list'.
    """

    data: list[ModelInfo]
    object_: Literal["list"] | Unset = "list"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        object_ = self.object_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_info import ModelInfo

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ModelInfo.from_dict(data_item_data)

            data.append(data_item)

        object_ = cast(Literal["list"] | Unset, d.pop("object", UNSET))
        if object_ != "list" and not isinstance(object_, Unset):
            raise ValueError(f"object must match const 'list', got '{object_}'")

        supported_models_response = cls(
            data=data,
            object_=object_,
        )

        supported_models_response.additional_properties = d
        return supported_models_response

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
