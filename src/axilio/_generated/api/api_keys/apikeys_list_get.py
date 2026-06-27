from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.apikey_api_key_list_response import ApikeyAPIKeyListResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api-keys",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApikeyAPIKeyListResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = ApikeyAPIKeyListResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApikeyAPIKeyListResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> Response[ApikeyAPIKeyListResponse | V2ErrorModel]:
    """List API keys (simple)

     Lists API keys for the caller's organization with simple limit/offset paging. Admin only. Use POST
    /api-keys/list for richer filters (search, created_by, sort).

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyListResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> ApikeyAPIKeyListResponse | V2ErrorModel | None:
    """List API keys (simple)

     Lists API keys for the caller's organization with simple limit/offset paging. Admin only. Use POST
    /api-keys/list for richer filters (search, created_by, sort).

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyListResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> Response[ApikeyAPIKeyListResponse | V2ErrorModel]:
    """List API keys (simple)

     Lists API keys for the caller's organization with simple limit/offset paging. Admin only. Use POST
    /api-keys/list for richer filters (search, created_by, sort).

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyListResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
) -> ApikeyAPIKeyListResponse | V2ErrorModel | None:
    """List API keys (simple)

     Lists API keys for the caller's organization with simple limit/offset paging. Admin only. Use POST
    /api-keys/list for richer filters (search, created_by, sort).

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyListResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
