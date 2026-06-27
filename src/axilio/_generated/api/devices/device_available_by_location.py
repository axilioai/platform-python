from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_available_phones_by_location_response import PhoneAvailablePhonesByLocationResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/available/by-location",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneAvailablePhonesByLocationResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneAvailablePhonesByLocationResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneAvailablePhonesByLocationResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[PhoneAvailablePhonesByLocationResponse | V2ErrorModel]:
    """Available device capacity by location

     Returns per-location capacity (available + max) across the device fleet. Powers the location picker
    in the workflow editor.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneAvailablePhonesByLocationResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> PhoneAvailablePhonesByLocationResponse | V2ErrorModel | None:
    """Available device capacity by location

     Returns per-location capacity (available + max) across the device fleet. Powers the location picker
    in the workflow editor.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneAvailablePhonesByLocationResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[PhoneAvailablePhonesByLocationResponse | V2ErrorModel]:
    """Available device capacity by location

     Returns per-location capacity (available + max) across the device fleet. Powers the location picker
    in the workflow editor.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneAvailablePhonesByLocationResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> PhoneAvailablePhonesByLocationResponse | V2ErrorModel | None:
    """Available device capacity by location

     Returns per-location capacity (available + max) across the device fleet. Powers the location picker
    in the workflow editor.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneAvailablePhonesByLocationResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
