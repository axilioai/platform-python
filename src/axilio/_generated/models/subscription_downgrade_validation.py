from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subscription_limit_impact import SubscriptionLimitImpact


T = TypeVar("T", bound="SubscriptionDowngradeValidation")


@_attrs_define
class SubscriptionDowngradeValidation:
    """
    Attributes:
        effective_date (datetime.datetime):
        errors (list[str] | None):
        is_valid (bool):
        limit_impacts (list[SubscriptionLimitImpact] | None):
        proration_amount (float):
        warnings (list[str] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    effective_date: datetime.datetime
    errors: list[str] | None
    is_valid: bool
    limit_impacts: list[SubscriptionLimitImpact] | None
    proration_amount: float
    warnings: list[str] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        effective_date = self.effective_date.isoformat()

        errors: list[str] | None
        if isinstance(self.errors, list):
            errors = self.errors

        else:
            errors = self.errors

        is_valid = self.is_valid

        limit_impacts: list[dict[str, Any]] | None
        if isinstance(self.limit_impacts, list):
            limit_impacts = []
            for limit_impacts_type_0_item_data in self.limit_impacts:
                limit_impacts_type_0_item = limit_impacts_type_0_item_data.to_dict()
                limit_impacts.append(limit_impacts_type_0_item)

        else:
            limit_impacts = self.limit_impacts

        proration_amount = self.proration_amount

        warnings: list[str] | None
        if isinstance(self.warnings, list):
            warnings = self.warnings

        else:
            warnings = self.warnings

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "effective_date": effective_date,
                "errors": errors,
                "is_valid": is_valid,
                "limit_impacts": limit_impacts,
                "proration_amount": proration_amount,
                "warnings": warnings,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.subscription_limit_impact import SubscriptionLimitImpact

        d = dict(src_dict)
        effective_date = datetime.datetime.fromisoformat(d.pop("effective_date"))

        def _parse_errors(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                errors_type_0 = cast(list[str], data)

                return errors_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        errors = _parse_errors(d.pop("errors"))

        is_valid = d.pop("is_valid")

        def _parse_limit_impacts(data: object) -> list[SubscriptionLimitImpact] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                limit_impacts_type_0 = []
                _limit_impacts_type_0 = data
                for limit_impacts_type_0_item_data in _limit_impacts_type_0:
                    limit_impacts_type_0_item = SubscriptionLimitImpact.from_dict(limit_impacts_type_0_item_data)

                    limit_impacts_type_0.append(limit_impacts_type_0_item)

                return limit_impacts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SubscriptionLimitImpact] | None, data)

        limit_impacts = _parse_limit_impacts(d.pop("limit_impacts"))

        proration_amount = d.pop("proration_amount")

        def _parse_warnings(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                warnings_type_0 = cast(list[str], data)

                return warnings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        warnings = _parse_warnings(d.pop("warnings"))

        schema = d.pop("$schema", UNSET)

        subscription_downgrade_validation = cls(
            effective_date=effective_date,
            errors=errors,
            is_valid=is_valid,
            limit_impacts=limit_impacts,
            proration_amount=proration_amount,
            warnings=warnings,
            schema=schema,
        )

        return subscription_downgrade_validation
