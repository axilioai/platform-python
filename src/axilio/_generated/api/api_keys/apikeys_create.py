from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.apikey_api_key_create_request import ApikeyAPIKeyCreateRequest
from ...models.apikey_api_key_create_response import ApikeyAPIKeyCreateResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    *,
    body: ApikeyAPIKeyCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-keys",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApikeyAPIKeyCreateResponse | V2ErrorModel:
    if response.status_code == 201:
        response_201 = ApikeyAPIKeyCreateResponse.from_dict(response.json())

        return response_201

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApikeyAPIKeyCreateResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ApikeyAPIKeyCreateRequest,
) -> Response[ApikeyAPIKeyCreateResponse | V2ErrorModel]:
    """Create an API key

     Mints a fresh API key for the caller's organization. Admin only. The plaintext key value is returned
    exactly once and never stored or returned again.

    Args:
        body (ApikeyAPIKeyCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyCreateResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ApikeyAPIKeyCreateRequest,
) -> ApikeyAPIKeyCreateResponse | V2ErrorModel | None:
    """Create an API key

     Mints a fresh API key for the caller's organization. Admin only. The plaintext key value is returned
    exactly once and never stored or returned again.

    Args:
        body (ApikeyAPIKeyCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyCreateResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ApikeyAPIKeyCreateRequest,
) -> Response[ApikeyAPIKeyCreateResponse | V2ErrorModel]:
    """Create an API key

     Mints a fresh API key for the caller's organization. Admin only. The plaintext key value is returned
    exactly once and never stored or returned again.

    Args:
        body (ApikeyAPIKeyCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyCreateResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ApikeyAPIKeyCreateRequest,
) -> ApikeyAPIKeyCreateResponse | V2ErrorModel | None:
    """Create an API key

     Mints a fresh API key for the caller's organization. Admin only. The plaintext key value is returned
    exactly once and never stored or returned again.

    Args:
        body (ApikeyAPIKeyCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyCreateResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
