from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_pricing import ModelPricing


T = TypeVar("T", bound="ModelInfo")


@_attrs_define
class ModelInfo:
    """One supported model and its pricing, as a standard /v1/models catalog row.

    Attributes:
        context_window (int): Maximum context window, in tokens.
        id (str): Model identifier, e.g. 'anthropic/claude-sonnet-4.5'. Pass this as `model` to /inference/locate.
        name (str): Human-readable model name.
        owned_by (str): Model provider, e.g. 'anthropic'.
        pricing (ModelPricing): Per-token price in USD — the customer's billed rate for a /locate call.
        type_ (str): Model type. 'vlm' for the vision-language models served by /locate.
        object_ (Literal['model'] | Unset):  Default: 'model'.
    """

    context_window: int
    id: str
    name: str
    owned_by: str
    pricing: ModelPricing
    type_: str
    object_: Literal["model"] | Unset = "model"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context_window = self.context_window

        id = self.id

        name = self.name

        owned_by = self.owned_by

        pricing = self.pricing.to_dict()

        type_ = self.type_

        object_ = self.object_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context_window": context_window,
                "id": id,
                "name": name,
                "owned_by": owned_by,
                "pricing": pricing,
                "type": type_,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_pricing import ModelPricing

        d = dict(src_dict)
        context_window = d.pop("context_window")

        id = d.pop("id")

        name = d.pop("name")

        owned_by = d.pop("owned_by")

        pricing = ModelPricing.from_dict(d.pop("pricing"))

        type_ = d.pop("type")

        object_ = cast(Literal["model"] | Unset, d.pop("object", UNSET))
        if object_ != "model" and not isinstance(object_, Unset):
            raise ValueError(f"object must match const 'model', got '{object_}'")

        model_info = cls(
            context_window=context_window,
            id=id,
            name=name,
            owned_by=owned_by,
            pricing=pricing,
            type_=type_,
            object_=object_,
        )

        model_info.additional_properties = d
        return model_info

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
