from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_phone_counts_response_android import PhonePhoneCountsResponseAndroid
    from ..models.phone_phone_counts_response_iphone import PhonePhoneCountsResponseIphone


T = TypeVar("T", bound="PhonePhoneCountsResponse")


@_attrs_define
class PhonePhoneCountsResponse:
    """
    Attributes:
        android (PhonePhoneCountsResponseAndroid):
        iphone (PhonePhoneCountsResponseIphone):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    android: PhonePhoneCountsResponseAndroid
    iphone: PhonePhoneCountsResponseIphone
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        android = self.android.to_dict()

        iphone = self.iphone.to_dict()

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "android": android,
                "iphone": iphone,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_phone_counts_response_android import PhonePhoneCountsResponseAndroid
        from ..models.phone_phone_counts_response_iphone import PhonePhoneCountsResponseIphone

        d = dict(src_dict)
        android = PhonePhoneCountsResponseAndroid.from_dict(d.pop("android"))

        iphone = PhonePhoneCountsResponseIphone.from_dict(d.pop("iphone"))

        schema = d.pop("$schema", UNSET)

        phone_phone_counts_response = cls(
            android=android,
            iphone=iphone,
            schema=schema,
        )

        return phone_phone_counts_response
