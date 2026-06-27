from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.supported_models_response import SupportedModelsResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/inference/models",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SupportedModelsResponse | None:
    if response.status_code == 200:
        response_200 = SupportedModelsResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SupportedModelsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[SupportedModelsResponse]:
    """List Models

     List the VLM models Argus supports for /locate.

    Public: no API key required (it's a catalog of model names, nothing
    sensitive), so a client can discover supported models before it holds
    credentials. The SDK fetches this once, caches it, and validates
    find(model=...) locally so a typo fails fast with a clean error instead
    of a 400 from /locate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SupportedModelsResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> SupportedModelsResponse | None:
    """List Models

     List the VLM models Argus supports for /locate.

    Public: no API key required (it's a catalog of model names, nothing
    sensitive), so a client can discover supported models before it holds
    credentials. The SDK fetches this once, caches it, and validates
    find(model=...) locally so a typo fails fast with a clean error instead
    of a 400 from /locate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SupportedModelsResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[SupportedModelsResponse]:
    """List Models

     List the VLM models Argus supports for /locate.

    Public: no API key required (it's a catalog of model names, nothing
    sensitive), so a client can discover supported models before it holds
    credentials. The SDK fetches this once, caches it, and validates
    find(model=...) locally so a typo fails fast with a clean error instead
    of a 400 from /locate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SupportedModelsResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> SupportedModelsResponse | None:
    """List Models

     List the VLM models Argus supports for /locate.

    Public: no API key required (it's a catalog of model names, nothing
    sensitive), so a client can discover supported models before it holds
    credentials. The SDK fetches this once, caches it, and validates
    find(model=...) locally so a typo fails fast with a clean error instead
    of a 400 from /locate.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SupportedModelsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
