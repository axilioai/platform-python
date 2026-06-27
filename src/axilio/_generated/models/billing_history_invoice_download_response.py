from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingHistoryInvoiceDownloadResponse")


@_attrs_define
class BillingHistoryInvoiceDownloadResponse:
    """
    Attributes:
        download_url (str):
        expires_at (datetime.datetime):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    download_url: str
    expires_at: datetime.datetime
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        download_url = self.download_url

        expires_at = self.expires_at.isoformat()

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "download_url": download_url,
                "expires_at": expires_at,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        download_url = d.pop("download_url")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        schema = d.pop("$schema", UNSET)

        billing_history_invoice_download_response = cls(
            download_url=download_url,
            expires_at=expires_at,
            schema=schema,
        )

        return billing_history_invoice_download_response
