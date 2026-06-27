from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationOrganizationCreateRequest")


@_attrs_define
class OrganizationOrganizationCreateRequest:
    """
    Attributes:
        external_org_id (str):
        name (str):
        slug (str):
        schema (str | Unset): A URL to the JSON Schema for this object.
        logo_url (str | Unset):
    """

    external_org_id: str
    name: str
    slug: str
    schema: str | Unset = UNSET
    logo_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        external_org_id = self.external_org_id

        name = self.name

        slug = self.slug

        schema = self.schema

        logo_url = self.logo_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "external_org_id": external_org_id,
                "name": name,
                "slug": slug,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        external_org_id = d.pop("external_org_id")

        name = d.pop("name")

        slug = d.pop("slug")

        schema = d.pop("$schema", UNSET)

        logo_url = d.pop("logo_url", UNSET)

        organization_organization_create_request = cls(
            external_org_id=external_org_id,
            name=name,
            slug=slug,
            schema=schema,
            logo_url=logo_url,
        )

        return organization_organization_create_request
