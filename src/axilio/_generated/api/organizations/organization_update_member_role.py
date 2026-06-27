from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.organization_organization_member_response import OrganizationOrganizationMemberResponse
from ...models.organization_update_org_member_role_request import OrganizationUpdateOrgMemberRoleRequest
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    org_id: str,
    user_id: str,
    *,
    body: OrganizationUpdateOrgMemberRoleRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/organizations/{org_id}/members/{user_id}".format(
            org_id=quote(str(org_id), safe=""),
            user_id=quote(str(user_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OrganizationOrganizationMemberResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = OrganizationOrganizationMemberResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OrganizationOrganizationMemberResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationUpdateOrgMemberRoleRequest,
) -> Response[OrganizationOrganizationMemberResponse | V2ErrorModel]:
    """Update a member's role

     Changes a member's role. Rejects changing your own role, and rejects downgrading the last admin. Org
    admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier whose role is being changed
        body (OrganizationUpdateOrgMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrganizationOrganizationMemberResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationUpdateOrgMemberRoleRequest,
) -> OrganizationOrganizationMemberResponse | V2ErrorModel | None:
    """Update a member's role

     Changes a member's role. Rejects changing your own role, and rejects downgrading the last admin. Org
    admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier whose role is being changed
        body (OrganizationUpdateOrgMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrganizationOrganizationMemberResponse | V2ErrorModel
    """

    return sync_detailed(
        org_id=org_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationUpdateOrgMemberRoleRequest,
) -> Response[OrganizationOrganizationMemberResponse | V2ErrorModel]:
    """Update a member's role

     Changes a member's role. Rejects changing your own role, and rejects downgrading the last admin. Org
    admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier whose role is being changed
        body (OrganizationUpdateOrgMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrganizationOrganizationMemberResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationUpdateOrgMemberRoleRequest,
) -> OrganizationOrganizationMemberResponse | V2ErrorModel | None:
    """Update a member's role

     Changes a member's role. Rejects changing your own role, and rejects downgrading the last admin. Org
    admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier whose role is being changed
        body (OrganizationUpdateOrgMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrganizationOrganizationMemberResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
