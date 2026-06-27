from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_success_response import PhoneSuccessResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    phone_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/phones/{phone_id}/wipe".format(
            phone_id=quote(str(phone_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneSuccessResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneSuccessResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneSuccessResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    phone_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PhoneSuccessResponse | V2ErrorModel]:
    """Wipe a private device on demand

     Requests an on-demand factory reset of a private device the caller's org owns. Requires the device
    to be ACTIVE and not currently allocated. Sets the device to MAINTENANCE while the wipe is carried
    out.

    Args:
        phone_id (str): device identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSuccessResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    phone_id: str,
    *,
    client: AuthenticatedClient,
) -> PhoneSuccessResponse | V2ErrorModel | None:
    """Wipe a private device on demand

     Requests an on-demand factory reset of a private device the caller's org owns. Requires the device
    to be ACTIVE and not currently allocated. Sets the device to MAINTENANCE while the wipe is carried
    out.

    Args:
        phone_id (str): device identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSuccessResponse | V2ErrorModel
    """

    return sync_detailed(
        phone_id=phone_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    phone_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PhoneSuccessResponse | V2ErrorModel]:
    """Wipe a private device on demand

     Requests an on-demand factory reset of a private device the caller's org owns. Requires the device
    to be ACTIVE and not currently allocated. Sets the device to MAINTENANCE while the wipe is carried
    out.

    Args:
        phone_id (str): device identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSuccessResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    phone_id: str,
    *,
    client: AuthenticatedClient,
) -> PhoneSuccessResponse | V2ErrorModel | None:
    """Wipe a private device on demand

     Requests an on-demand factory reset of a private device the caller's org owns. Requires the device
    to be ACTIVE and not currently allocated. Sets the device to MAINTENANCE while the wipe is carried
    out.

    Args:
        phone_id (str): device identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSuccessResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            phone_id=phone_id,
            client=client,
        )
    ).parsed
