from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingHistoryInvoiceDownloadRequest")


@_attrs_define
class BillingHistoryInvoiceDownloadRequest:
    """
    Attributes:
        invoice_id (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    invoice_id: str
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        invoice_id = self.invoice_id

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "invoice_id": invoice_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        invoice_id = d.pop("invoice_id")

        schema = d.pop("$schema", UNSET)

        billing_history_invoice_download_request = cls(
            invoice_id=invoice_id,
            schema=schema,
        )

        return billing_history_invoice_download_request
