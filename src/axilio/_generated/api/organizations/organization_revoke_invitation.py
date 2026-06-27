from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.message_output_body import MessageOutputBody
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    org_id: str,
    invitation_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/organizations/{org_id}/invitations/{invitation_id}".format(
            org_id=quote(str(org_id), safe=""),
            invitation_id=quote(str(invitation_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> MessageOutputBody | V2ErrorModel:
    if response.status_code == 200:
        response_200 = MessageOutputBody.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MessageOutputBody | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[MessageOutputBody | V2ErrorModel]:
    """Revoke an invitation

     Revokes an outstanding invitation and deletes the local record. Org admin only.

    Args:
        org_id (str): organization identifier
        invitation_id (str): invitation identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageOutputBody | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        invitation_id=invitation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> MessageOutputBody | V2ErrorModel | None:
    """Revoke an invitation

     Revokes an outstanding invitation and deletes the local record. Org admin only.

    Args:
        org_id (str): organization identifier
        invitation_id (str): invitation identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageOutputBody | V2ErrorModel
    """

    return sync_detailed(
        org_id=org_id,
        invitation_id=invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[MessageOutputBody | V2ErrorModel]:
    """Revoke an invitation

     Revokes an outstanding invitation and deletes the local record. Org admin only.

    Args:
        org_id (str): organization identifier
        invitation_id (str): invitation identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageOutputBody | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        invitation_id=invitation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    invitation_id: str,
    *,
    client: AuthenticatedClient,
) -> MessageOutputBody | V2ErrorModel | None:
    """Revoke an invitation

     Revokes an outstanding invitation and deletes the local record. Org admin only.

    Args:
        org_id (str): organization identifier
        invitation_id (str): invitation identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageOutputBody | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            invitation_id=invitation_id,
            client=client,
        )
    ).parsed
