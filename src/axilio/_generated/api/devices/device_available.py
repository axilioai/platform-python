from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_available_phones_response import PhoneAvailablePhonesResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    device_type: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["device_type"] = device_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/available",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneAvailablePhonesResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneAvailablePhonesResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneAvailablePhonesResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    device_type: str | Unset = UNSET,
) -> Response[PhoneAvailablePhonesResponse | V2ErrorModel]:
    """List available devices

     Returns ACTIVE unallocated devices the caller's org can claim, optionally filtered by device type
    (iphone/android). Counts by type are included alongside the list.

    Args:
        device_type (str | Unset): filter by device type (iphone/android)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneAvailablePhonesResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        device_type=device_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    device_type: str | Unset = UNSET,
) -> PhoneAvailablePhonesResponse | V2ErrorModel | None:
    """List available devices

     Returns ACTIVE unallocated devices the caller's org can claim, optionally filtered by device type
    (iphone/android). Counts by type are included alongside the list.

    Args:
        device_type (str | Unset): filter by device type (iphone/android)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneAvailablePhonesResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        device_type=device_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    device_type: str | Unset = UNSET,
) -> Response[PhoneAvailablePhonesResponse | V2ErrorModel]:
    """List available devices

     Returns ACTIVE unallocated devices the caller's org can claim, optionally filtered by device type
    (iphone/android). Counts by type are included alongside the list.

    Args:
        device_type (str | Unset): filter by device type (iphone/android)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneAvailablePhonesResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        device_type=device_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    device_type: str | Unset = UNSET,
) -> PhoneAvailablePhonesResponse | V2ErrorModel | None:
    """List available devices

     Returns ACTIVE unallocated devices the caller's org can claim, optionally filtered by device type
    (iphone/android). Counts by type are included alongside the list.

    Args:
        device_type (str | Unset): filter by device type (iphone/android)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneAvailablePhonesResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            device_type=device_type,
        )
    ).parsed
