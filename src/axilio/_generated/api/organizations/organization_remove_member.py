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
    user_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/organizations/{org_id}/members/{user_id}".format(
            org_id=quote(str(org_id), safe=""),
            user_id=quote(str(user_id), safe=""),
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
    user_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[MessageOutputBody | V2ErrorModel]:
    """Remove an organization member

     Removes a user from the organization. Rejects removing yourself, and rejects removing the last admin
    of an organization. Org admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier to remove

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageOutputBody | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        user_id=user_id,
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
) -> MessageOutputBody | V2ErrorModel | None:
    """Remove an organization member

     Removes a user from the organization. Rejects removing yourself, and rejects removing the last admin
    of an organization. Org admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier to remove

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageOutputBody | V2ErrorModel
    """

    return sync_detailed(
        org_id=org_id,
        user_id=user_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[MessageOutputBody | V2ErrorModel]:
    """Remove an organization member

     Removes a user from the organization. Rejects removing yourself, and rejects removing the last admin
    of an organization. Org admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier to remove

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageOutputBody | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
) -> MessageOutputBody | V2ErrorModel | None:
    """Remove an organization member

     Removes a user from the organization. Rejects removing yourself, and rejects removing the last admin
    of an organization. Org admin only.

    Args:
        org_id (str): organization identifier
        user_id (str): user identifier to remove

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageOutputBody | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            user_id=user_id,
            client=client,
        )
    ).parsed
