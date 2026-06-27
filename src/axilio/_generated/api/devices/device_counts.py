from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_phone_counts_response import PhonePhoneCountsResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response


def _get_kwargs(
    *,
    device_status: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["device_status"] = device_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/counts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhonePhoneCountsResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhonePhoneCountsResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhonePhoneCountsResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    device_status: str,
) -> Response[PhonePhoneCountsResponse | V2ErrorModel]:
    """Count devices by type for a status

     Returns device counts grouped by type (iphone/android) for the given status
    (ACTIVE/INACTIVE/MAINTENANCE).

    Args:
        device_status (str): device status to count (ACTIVE/INACTIVE/MAINTENANCE)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhonePhoneCountsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        device_status=device_status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    device_status: str,
) -> PhonePhoneCountsResponse | V2ErrorModel | None:
    """Count devices by type for a status

     Returns device counts grouped by type (iphone/android) for the given status
    (ACTIVE/INACTIVE/MAINTENANCE).

    Args:
        device_status (str): device status to count (ACTIVE/INACTIVE/MAINTENANCE)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhonePhoneCountsResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        device_status=device_status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    device_status: str,
) -> Response[PhonePhoneCountsResponse | V2ErrorModel]:
    """Count devices by type for a status

     Returns device counts grouped by type (iphone/android) for the given status
    (ACTIVE/INACTIVE/MAINTENANCE).

    Args:
        device_status (str): device status to count (ACTIVE/INACTIVE/MAINTENANCE)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhonePhoneCountsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        device_status=device_status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    device_status: str,
) -> PhonePhoneCountsResponse | V2ErrorModel | None:
    """Count devices by type for a status

     Returns device counts grouped by type (iphone/android) for the given status
    (ACTIVE/INACTIVE/MAINTENANCE).

    Args:
        device_status (str): device status to count (ACTIVE/INACTIVE/MAINTENANCE)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhonePhoneCountsResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            device_status=device_status,
        )
    ).parsed
