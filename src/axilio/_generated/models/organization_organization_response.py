from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationOrganizationResponse")


@_attrs_define
class OrganizationOrganizationResponse:
    """
    Attributes:
        balance_microdollars (int):
        external_org_id (str):
        id (str):
        name (str):
        slug (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        created_at (datetime.datetime | Unset):
        logo_url (str | Unset):
        onboarding_completed_at (datetime.datetime | Unset):
    """

    balance_microdollars: int
    external_org_id: str
    id: str
    name: str
    slug: str
    schema: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    logo_url: str | Unset = UNSET
    onboarding_completed_at: datetime.datetime | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        balance_microdollars = self.balance_microdollars

        external_org_id = self.external_org_id

        id = self.id

        name = self.name

        slug = self.slug

        schema = self.schema

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        logo_url = self.logo_url

        onboarding_completed_at: str | Unset = UNSET
        if not isinstance(self.onboarding_completed_at, Unset):
            onboarding_completed_at = self.onboarding_completed_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "balance_microdollars": balance_microdollars,
                "external_org_id": external_org_id,
                "id": id,
                "name": name,
                "slug": slug,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if onboarding_completed_at is not UNSET:
            field_dict["onboarding_completed_at"] = onboarding_completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        balance_microdollars = d.pop("balance_microdollars")

        external_org_id = d.pop("external_org_id")

        id = d.pop("id")

        name = d.pop("name")

        slug = d.pop("slug")

        schema = d.pop("$schema", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)

        logo_url = d.pop("logo_url", UNSET)

        _onboarding_completed_at = d.pop("onboarding_completed_at", UNSET)
        onboarding_completed_at: datetime.datetime | Unset
        if isinstance(_onboarding_completed_at, Unset):
            onboarding_completed_at = UNSET
        else:
            onboarding_completed_at = datetime.datetime.fromisoformat(_onboarding_completed_at)

        organization_organization_response = cls(
            balance_microdollars=balance_microdollars,
            external_org_id=external_org_id,
            id=id,
            name=name,
            slug=slug,
            schema=schema,
            created_at=created_at,
            logo_url=logo_url,
            onboarding_completed_at=onboarding_completed_at,
        )

        return organization_organization_response
