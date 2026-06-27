from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.user_settings_user_settings_update_request import UserSettingsUserSettingsUpdateRequest
from ...models.user_settings_user_settings_update_response import UserSettingsUserSettingsUpdateResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    *,
    body: UserSettingsUserSettingsUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/user-settings",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> UserSettingsUserSettingsUpdateResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = UserSettingsUserSettingsUpdateResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[UserSettingsUserSettingsUpdateResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: UserSettingsUserSettingsUpdateRequest,
) -> Response[UserSettingsUserSettingsUpdateResponse | V2ErrorModel]:
    """Update user settings

     Applies a partial update to the caller's API key settings. A nil field leaves the column unchanged;
    an empty string clears it; a value replaces it. Writes fail with a 500 if the server-side encryption
    key is not configured.

    Args:
        body (UserSettingsUserSettingsUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserSettingsUserSettingsUpdateResponse | V2ErrorModel]
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
    body: UserSettingsUserSettingsUpdateRequest,
) -> UserSettingsUserSettingsUpdateResponse | V2ErrorModel | None:
    """Update user settings

     Applies a partial update to the caller's API key settings. A nil field leaves the column unchanged;
    an empty string clears it; a value replaces it. Writes fail with a 500 if the server-side encryption
    key is not configured.

    Args:
        body (UserSettingsUserSettingsUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserSettingsUserSettingsUpdateResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: UserSettingsUserSettingsUpdateRequest,
) -> Response[UserSettingsUserSettingsUpdateResponse | V2ErrorModel]:
    """Update user settings

     Applies a partial update to the caller's API key settings. A nil field leaves the column unchanged;
    an empty string clears it; a value replaces it. Writes fail with a 500 if the server-side encryption
    key is not configured.

    Args:
        body (UserSettingsUserSettingsUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserSettingsUserSettingsUpdateResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: UserSettingsUserSettingsUpdateRequest,
) -> UserSettingsUserSettingsUpdateResponse | V2ErrorModel | None:
    """Update user settings

     Applies a partial update to the caller's API key settings. A nil field leaves the column unchanged;
    an empty string clears it; a value replaces it. Writes fail with a 500 if the server-side encryption
    key is not configured.

    Args:
        body (UserSettingsUserSettingsUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserSettingsUserSettingsUpdateResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
