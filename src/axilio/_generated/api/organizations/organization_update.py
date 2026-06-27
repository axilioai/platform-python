from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.organization_organization_response import OrganizationOrganizationResponse
from ...models.organization_organization_update_request import OrganizationOrganizationUpdateRequest
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    org_id: str,
    *,
    body: OrganizationOrganizationUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/organizations/{org_id}".format(
            org_id=quote(str(org_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OrganizationOrganizationResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = OrganizationOrganizationResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OrganizationOrganizationResponse | V2ErrorModel]:
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
    body: OrganizationOrganizationUpdateRequest,
) -> Response[OrganizationOrganizationResponse | V2ErrorModel]:
    """Update an organization

     Applies a partial update (name, slug, logo). Also marks onboarding complete the first time name or
    slug is set. Org admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationOrganizationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrganizationOrganizationResponse | V2ErrorModel]
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
    body: OrganizationOrganizationUpdateRequest,
) -> OrganizationOrganizationResponse | V2ErrorModel | None:
    """Update an organization

     Applies a partial update (name, slug, logo). Also marks onboarding complete the first time name or
    slug is set. Org admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationOrganizationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrganizationOrganizationResponse | V2ErrorModel
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
    body: OrganizationOrganizationUpdateRequest,
) -> Response[OrganizationOrganizationResponse | V2ErrorModel]:
    """Update an organization

     Applies a partial update (name, slug, logo). Also marks onboarding complete the first time name or
    slug is set. Org admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationOrganizationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrganizationOrganizationResponse | V2ErrorModel]
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
    body: OrganizationOrganizationUpdateRequest,
) -> OrganizationOrganizationResponse | V2ErrorModel | None:
    """Update an organization

     Applies a partial update (name, slug, logo). Also marks onboarding complete the first time name or
    slug is set. Org admin only.

    Args:
        org_id (str): organization identifier
        body (OrganizationOrganizationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrganizationOrganizationResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
