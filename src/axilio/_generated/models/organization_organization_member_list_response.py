from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_organization_member_response import OrganizationOrganizationMemberResponse


T = TypeVar("T", bound="OrganizationOrganizationMemberListResponse")


@_attrs_define
class OrganizationOrganizationMemberListResponse:
    """
    Attributes:
        members (list[OrganizationOrganizationMemberResponse] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    members: list[OrganizationOrganizationMemberResponse] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        members: list[dict[str, Any]] | None
        if isinstance(self.members, list):
            members = []
            for members_type_0_item_data in self.members:
                members_type_0_item = members_type_0_item_data.to_dict()
                members.append(members_type_0_item)

        else:
            members = self.members

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "members": members,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_organization_member_response import OrganizationOrganizationMemberResponse

        d = dict(src_dict)

        def _parse_members(data: object) -> list[OrganizationOrganizationMemberResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                members_type_0 = []
                _members_type_0 = data
                for members_type_0_item_data in _members_type_0:
                    members_type_0_item = OrganizationOrganizationMemberResponse.from_dict(members_type_0_item_data)

                    members_type_0.append(members_type_0_item)

                return members_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[OrganizationOrganizationMemberResponse] | None, data)

        members = _parse_members(d.pop("members"))

        schema = d.pop("$schema", UNSET)

        organization_organization_member_list_response = cls(
            members=members,
            schema=schema,
        )

        return organization_organization_member_list_response
