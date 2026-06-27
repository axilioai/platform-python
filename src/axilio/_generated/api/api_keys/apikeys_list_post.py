from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.apikey_api_key_list_request import ApikeyAPIKeyListRequest
from ...models.apikey_api_key_list_response import ApikeyAPIKeyListResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    *,
    body: ApikeyAPIKeyListRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-keys/list",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: ApikeyAPIKeyListRequest,
) -> Response[ApikeyAPIKeyListResponse | V2ErrorModel]:
    """List API keys (rich filters)

     Lists API keys with full filter and sort options in the request body. Admin only.

    Args:
        body (ApikeyAPIKeyListRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyListResponse | V2ErrorModel]
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
    body: ApikeyAPIKeyListRequest,
) -> ApikeyAPIKeyListResponse | V2ErrorModel | None:
    """List API keys (rich filters)

     Lists API keys with full filter and sort options in the request body. Admin only.

    Args:
        body (ApikeyAPIKeyListRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyListResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ApikeyAPIKeyListRequest,
) -> Response[ApikeyAPIKeyListResponse | V2ErrorModel]:
    """List API keys (rich filters)

     Lists API keys with full filter and sort options in the request body. Admin only.

    Args:
        body (ApikeyAPIKeyListRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApikeyAPIKeyListResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ApikeyAPIKeyListRequest,
) -> ApikeyAPIKeyListResponse | V2ErrorModel | None:
    """List API keys (rich filters)

     Lists API keys with full filter and sort options in the request body. Admin only.

    Args:
        body (ApikeyAPIKeyListRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApikeyAPIKeyListResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
