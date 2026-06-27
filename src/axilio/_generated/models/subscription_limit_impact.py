from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SubscriptionLimitImpact")


@_attrs_define
class SubscriptionLimitImpact:
    """
    Attributes:
        current_value (Any):
        feature (str):
        impact (str):
        is_reduction (bool):
        new_value (Any):
    """

    current_value: Any
    feature: str
    impact: str
    is_reduction: bool
    new_value: Any

    def to_dict(self) -> dict[str, Any]:
        current_value = self.current_value

        feature = self.feature

        impact = self.impact

        is_reduction = self.is_reduction

        new_value = self.new_value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "current_value": current_value,
                "feature": feature,
                "impact": impact,
                "is_reduction": is_reduction,
                "new_value": new_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        current_value = d.pop("current_value")

        feature = d.pop("feature")

        impact = d.pop("impact")

        is_reduction = d.pop("is_reduction")

        new_value = d.pop("new_value")

        subscription_limit_impact = cls(
            current_value=current_value,
            feature=feature,
            impact=impact,
            is_reduction=is_reduction,
            new_value=new_value,
        )

        return subscription_limit_impact
