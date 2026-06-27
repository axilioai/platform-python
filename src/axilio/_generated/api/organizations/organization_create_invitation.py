from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.organization_create_invitation_request import OrganizationCreateInvitationRequest
from ...models.organization_invitation_response import OrganizationInvitationResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    org_id: str,
    *,
    body: OrganizationCreateInvitationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/organizations/{org_id}/invitations".format(
            org_id=quote(str(org_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OrganizationInvitationResponse | V2ErrorModel:
    if response.status_code == 201:
        response_201 = OrganizationInvitationResponse.from_dict(response.json())

        return response_201

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OrganizationInvitationResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationCreateInvitationRequest,
) -> Response[OrganizationInvitationResponse | V2ErrorModel]:
    """Invite a user to an organization

     Creates an organization invitation. Idempotent by org_id + email: rejects 409 on duplicate. Org
    admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationCreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrganizationInvitationResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationCreateInvitationRequest,
) -> OrganizationInvitationResponse | V2ErrorModel | None:
    """Invite a user to an organization

     Creates an organization invitation. Idempotent by org_id + email: rejects 409 on duplicate. Org
    admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationCreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrganizationInvitationResponse | V2ErrorModel
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationCreateInvitationRequest,
) -> Response[OrganizationInvitationResponse | V2ErrorModel]:
    """Invite a user to an organization

     Creates an organization invitation. Idempotent by org_id + email: rejects 409 on duplicate. Org
    admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationCreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrganizationInvitationResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient,
    body: OrganizationCreateInvitationRequest,
) -> OrganizationInvitationResponse | V2ErrorModel | None:
    """Invite a user to an organization

     Creates an organization invitation. Idempotent by org_id + email: rejects 409 on duplicate. Org
    admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationCreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrganizationInvitationResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
