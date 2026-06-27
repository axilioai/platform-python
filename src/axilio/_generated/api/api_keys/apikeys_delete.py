from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.delete_api_key_output_body import DeleteAPIKeyOutputBody
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    key_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api-keys/{key_id}".format(
            key_id=quote(str(key_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteAPIKeyOutputBody | V2ErrorModel:
    if response.status_code == 200:
        response_200 = DeleteAPIKeyOutputBody.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DeleteAPIKeyOutputBody | V2ErrorModel]:
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
) -> Response[DeleteAPIKeyOutputBody | V2ErrorModel]:
    """Delete an API key

     Revokes an API key. Subsequent requests using its value are rejected as unauthorized. Admin only.

    Args:
        key_id (str): API key identifier to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteAPIKeyOutputBody | V2ErrorModel]
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
) -> DeleteAPIKeyOutputBody | V2ErrorModel | None:
    """Delete an API key

     Revokes an API key. Subsequent requests using its value are rejected as unauthorized. Admin only.

    Args:
        key_id (str): API key identifier to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteAPIKeyOutputBody | V2ErrorModel
    """

    return sync_detailed(
        key_id=key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    key_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[DeleteAPIKeyOutputBody | V2ErrorModel]:
    """Delete an API key

     Revokes an API key. Subsequent requests using its value are rejected as unauthorized. Admin only.

    Args:
        key_id (str): API key identifier to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteAPIKeyOutputBody | V2ErrorModel]
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
) -> DeleteAPIKeyOutputBody | V2ErrorModel | None:
    """Delete an API key

     Revokes an API key. Subsequent requests using its value are rejected as unauthorized. Admin only.

    Args:
        key_id (str): API key identifier to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteAPIKeyOutputBody | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            key_id=key_id,
            client=client,
        )
    ).parsed
