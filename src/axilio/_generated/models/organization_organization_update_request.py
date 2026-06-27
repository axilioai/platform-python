from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationOrganizationUpdateRequest")


@_attrs_define
class OrganizationOrganizationUpdateRequest:
    """
    Attributes:
        schema (str | Unset): A URL to the JSON Schema for this object.
        logo_url (str | Unset):
        name (str | Unset):
        slug (str | Unset):
    """

    schema: str | Unset = UNSET
    logo_url: str | Unset = UNSET
    name: str | Unset = UNSET
    slug: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        logo_url = self.logo_url

        name = self.name

        slug = self.slug

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        logo_url = d.pop("logo_url", UNSET)

        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        organization_organization_update_request = cls(
            schema=schema,
            logo_url=logo_url,
            name=name,
            slug=slug,
        )

        return organization_organization_update_request
