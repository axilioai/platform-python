from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_invitation_response import OrganizationInvitationResponse


T = TypeVar("T", bound="OrganizationInvitationListResponse")


@_attrs_define
class OrganizationInvitationListResponse:
    """
    Attributes:
        invitations (list[OrganizationInvitationResponse] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    invitations: list[OrganizationInvitationResponse] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        invitations: list[dict[str, Any]] | None
        if isinstance(self.invitations, list):
            invitations = []
            for invitations_type_0_item_data in self.invitations:
                invitations_type_0_item = invitations_type_0_item_data.to_dict()
                invitations.append(invitations_type_0_item)

        else:
            invitations = self.invitations

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "invitations": invitations,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization_invitation_response import OrganizationInvitationResponse

        d = dict(src_dict)

        def _parse_invitations(data: object) -> list[OrganizationInvitationResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                invitations_type_0 = []
                _invitations_type_0 = data
                for invitations_type_0_item_data in _invitations_type_0:
                    invitations_type_0_item = OrganizationInvitationResponse.from_dict(invitations_type_0_item_data)

                    invitations_type_0.append(invitations_type_0_item)

                return invitations_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[OrganizationInvitationResponse] | None, data)

        invitations = _parse_invitations(d.pop("invitations"))

        schema = d.pop("$schema", UNSET)

        organization_invitation_list_response = cls(
            invitations=invitations,
            schema=schema,
        )

        return organization_invitation_list_response
