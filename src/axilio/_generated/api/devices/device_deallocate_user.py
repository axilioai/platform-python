from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_deallocate_phone_response import PhoneDeallocatePhoneResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response


def _get_kwargs(
    *,
    phone_id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["phone_id"] = phone_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/phones/user/deallocate",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneDeallocatePhoneResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneDeallocatePhoneResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneDeallocatePhoneResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    phone_id: str,
) -> Response[PhoneDeallocatePhoneResponse | V2ErrorModel]:
    """User-initiated deallocation

     Deallocates a device the caller's org currently holds. The session is billed and the device is torn
    down asynchronously.

    Args:
        phone_id (str): device identifier to deallocate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneDeallocatePhoneResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    phone_id: str,
) -> PhoneDeallocatePhoneResponse | V2ErrorModel | None:
    """User-initiated deallocation

     Deallocates a device the caller's org currently holds. The session is billed and the device is torn
    down asynchronously.

    Args:
        phone_id (str): device identifier to deallocate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneDeallocatePhoneResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        phone_id=phone_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    phone_id: str,
) -> Response[PhoneDeallocatePhoneResponse | V2ErrorModel]:
    """User-initiated deallocation

     Deallocates a device the caller's org currently holds. The session is billed and the device is torn
    down asynchronously.

    Args:
        phone_id (str): device identifier to deallocate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneDeallocatePhoneResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    phone_id: str,
) -> PhoneDeallocatePhoneResponse | V2ErrorModel | None:
    """User-initiated deallocation

     Deallocates a device the caller's org currently holds. The session is billed and the device is torn
    down asynchronously.

    Args:
        phone_id (str): device identifier to deallocate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneDeallocatePhoneResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            phone_id=phone_id,
        )
    ).parsed
