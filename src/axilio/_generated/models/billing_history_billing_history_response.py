from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_history_billing_history_item import BillingHistoryBillingHistoryItem


T = TypeVar("T", bound="BillingHistoryBillingHistoryResponse")


@_attrs_define
class BillingHistoryBillingHistoryResponse:
    """
    Attributes:
        has_more (bool):
        items (list[BillingHistoryBillingHistoryItem] | None):
        total_count (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    has_more: bool
    items: list[BillingHistoryBillingHistoryItem] | None
    total_count: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        has_more = self.has_more

        items: list[dict[str, Any]] | None
        if isinstance(self.items, list):
            items = []
            for items_type_0_item_data in self.items:
                items_type_0_item = items_type_0_item_data.to_dict()
                items.append(items_type_0_item)

        else:
            items = self.items

        total_count = self.total_count

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "has_more": has_more,
                "items": items,
                "total_count": total_count,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_history_billing_history_item import BillingHistoryBillingHistoryItem

        d = dict(src_dict)
        has_more = d.pop("has_more")

        def _parse_items(data: object) -> list[BillingHistoryBillingHistoryItem] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                items_type_0 = []
                _items_type_0 = data
                for items_type_0_item_data in _items_type_0:
                    items_type_0_item = BillingHistoryBillingHistoryItem.from_dict(items_type_0_item_data)

                    items_type_0.append(items_type_0_item)

                return items_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[BillingHistoryBillingHistoryItem] | None, data)

        items = _parse_items(d.pop("items"))

        total_count = d.pop("total_count")

        schema = d.pop("$schema", UNSET)

        billing_history_billing_history_response = cls(
            has_more=has_more,
            items=items,
            total_count=total_count,
            schema=schema,
        )

        return billing_history_billing_history_response
