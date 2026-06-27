from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.apikey_api_key_regenerate_response import ApikeyAPIKeyRegenerateResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    key_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-keys/{key_id}/regenerate".format(
            key_id=quote(str(key_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApikeyAPIKeyRegenerateResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = ApikeyAPIKeyRegenerateResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApikeyAPIKeyRegenerateResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    key_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ApikeyAPIKeyRegenerateResponse | V2ErrorModel]:
    """Regenerate an API key

     Rotates the plaintext value for an existing API key, preserving its name and identifier. The
    previous value is invalidated immediately. Admin only.

    Args:
        key_id (str): API key identifier to regenerate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyRegenerateResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        key_id=key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    key_id: str,
    *,
    client: AuthenticatedClient,
) -> ApikeyAPIKeyRegenerateResponse | V2ErrorModel | None:
    """Regenerate an API key

     Rotates the plaintext value for an existing API key, preserving its name and identifier. The
    previous value is invalidated immediately. Admin only.

    Args:
        key_id (str): API key identifier to regenerate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyRegenerateResponse | V2ErrorModel
    """

    return sync_detailed(
        key_id=key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    key_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ApikeyAPIKeyRegenerateResponse | V2ErrorModel]:
    """Regenerate an API key

     Rotates the plaintext value for an existing API key, preserving its name and identifier. The
    previous value is invalidated immediately. Admin only.

    Args:
        key_id (str): API key identifier to regenerate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyRegenerateResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        key_id=key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    key_id: str,
    *,
    client: AuthenticatedClient,
) -> ApikeyAPIKeyRegenerateResponse | V2ErrorModel | None:
    """Regenerate an API key

     Rotates the plaintext value for an existing API key, preserving its name and identifier. The
    previous value is invalidated immediately. Admin only.

    Args:
        key_id (str): API key identifier to regenerate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyRegenerateResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            key_id=key_id,
            client=client,
        )
    ).parsed
