from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_supported_phone_apps_response import PhoneSupportedPhoneAppsResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    platform: str | Unset = UNSET,
    category: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["platform"] = platform

    params["category"] = category

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/device-apps/supported",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneSupportedPhoneAppsResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneSupportedPhoneAppsResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneSupportedPhoneAppsResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    platform: str | Unset = UNSET,
    category: str | Unset = UNSET,
) -> Response[PhoneSupportedPhoneAppsResponse | V2ErrorModel]:
    """List supported device apps

     Returns the apps the platform supports orchestration for, optionally filtered by platform +
    category. Platform admins see internal/unreleased apps too.

    Args:
        platform (str | Unset): filter by platform
        category (str | Unset): filter by app category

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSupportedPhoneAppsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        platform=platform,
        category=category,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    platform: str | Unset = UNSET,
    category: str | Unset = UNSET,
) -> PhoneSupportedPhoneAppsResponse | V2ErrorModel | None:
    """List supported device apps

     Returns the apps the platform supports orchestration for, optionally filtered by platform +
    category. Platform admins see internal/unreleased apps too.

    Args:
        platform (str | Unset): filter by platform
        category (str | Unset): filter by app category

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSupportedPhoneAppsResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        platform=platform,
        category=category,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    platform: str | Unset = UNSET,
    category: str | Unset = UNSET,
) -> Response[PhoneSupportedPhoneAppsResponse | V2ErrorModel]:
    """List supported device apps

     Returns the apps the platform supports orchestration for, optionally filtered by platform +
    category. Platform admins see internal/unreleased apps too.

    Args:
        platform (str | Unset): filter by platform
        category (str | Unset): filter by app category

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSupportedPhoneAppsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        platform=platform,
        category=category,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    platform: str | Unset = UNSET,
    category: str | Unset = UNSET,
) -> PhoneSupportedPhoneAppsResponse | V2ErrorModel | None:
    """List supported device apps

     Returns the apps the platform supports orchestration for, optionally filtered by platform +
    category. Platform admins see internal/unreleased apps too.

    Args:
        platform (str | Unset): filter by platform
        category (str | Unset): filter by app category

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSupportedPhoneAppsResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            platform=platform,
            category=category,
        )
    ).parsed
