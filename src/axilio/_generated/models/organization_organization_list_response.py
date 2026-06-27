from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_organization_response import OrganizationOrganizationResponse


T = TypeVar("T", bound="OrganizationOrganizationListResponse")


@_attrs_define
class OrganizationOrganizationListResponse:
    """
    Attributes:
        organizations (list[OrganizationOrganizationResponse] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    organizations: list[OrganizationOrganizationResponse] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        organizations: list[dict[str, Any]] | None
        if isinstance(self.organizations, list):
            organizations = []
            for organizations_type_0_item_data in self.organizations:
                organizations_type_0_item = organizations_type_0_item_data.to_dict()
                organizations.append(organizations_type_0_item)

        else:
            organizations = self.organizations

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "organizations": organizations,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_organization_response import OrganizationOrganizationResponse

        d = dict(src_dict)

        def _parse_organizations(data: object) -> list[OrganizationOrganizationResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                organizations_type_0 = []
                _organizations_type_0 = data
                for organizations_type_0_item_data in _organizations_type_0:
                    organizations_type_0_item = OrganizationOrganizationResponse.from_dict(
                        organizations_type_0_item_data
                    )

                    organizations_type_0.append(organizations_type_0_item)

                return organizations_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[OrganizationOrganizationResponse] | None, data)

        organizations = _parse_organizations(d.pop("organizations"))

        schema = d.pop("$schema", UNSET)

        organization_organization_list_response = cls(
            organizations=organizations,
            schema=schema,
        )

        return organization_organization_list_response
