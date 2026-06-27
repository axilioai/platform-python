from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_phone_summary import PhonePhoneSummary
from ...models.phone_update_nickname_request import PhoneUpdateNicknameRequest
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    phone_id: str,
    *,
    body: PhoneUpdateNicknameRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/phones/{phone_id}/nickname".format(
            phone_id=quote(str(phone_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhonePhoneSummary | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhonePhoneSummary.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhonePhoneSummary | V2ErrorModel]:
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
    body: PhoneUpdateNicknameRequest,
) -> Response[PhonePhoneSummary | V2ErrorModel]:
    """Set a private device's nickname

     Sets the human-readable display name on a private device the caller's org owns. Returns the updated
    device summary.

    Args:
        phone_id (str): device identifier
        body (PhoneUpdateNicknameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhonePhoneSummary | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    phone_id: str,
    *,
    client: AuthenticatedClient,
    body: PhoneUpdateNicknameRequest,
) -> PhonePhoneSummary | V2ErrorModel | None:
    """Set a private device's nickname

     Sets the human-readable display name on a private device the caller's org owns. Returns the updated
    device summary.

    Args:
        phone_id (str): device identifier
        body (PhoneUpdateNicknameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhonePhoneSummary | V2ErrorModel
    """

    return sync_detailed(
        phone_id=phone_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    phone_id: str,
    *,
    client: AuthenticatedClient,
    body: PhoneUpdateNicknameRequest,
) -> Response[PhonePhoneSummary | V2ErrorModel]:
    """Set a private device's nickname

     Sets the human-readable display name on a private device the caller's org owns. Returns the updated
    device summary.

    Args:
        phone_id (str): device identifier
        body (PhoneUpdateNicknameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhonePhoneSummary | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    phone_id: str,
    *,
    client: AuthenticatedClient,
    body: PhoneUpdateNicknameRequest,
) -> PhonePhoneSummary | V2ErrorModel | None:
    """Set a private device's nickname

     Sets the human-readable display name on a private device the caller's org owns. Returns the updated
    device summary.

    Args:
        phone_id (str): device identifier
        body (PhoneUpdateNicknameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhonePhoneSummary | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            phone_id=phone_id,
            client=client,
            body=body,
        )
    ).parsed
