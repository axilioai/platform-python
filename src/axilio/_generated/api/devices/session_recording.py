from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_session_recording_response import PhoneSessionRecordingResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/sessions/{id}/recording".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneSessionRecordingResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneSessionRecordingResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneSessionRecordingResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PhoneSessionRecordingResponse | V2ErrorModel]:
    r"""Get a session's screen recording URL

     Returns a short-lived URL for the session's screen recording, keyed on session_id — so it works for
    workflow runs and workflow-less interactive leases alike. Status is \"pending\" (no URL) when the
    recording hasn't finished uploading yet. Org-scoped: another org's session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSessionRecordingResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> PhoneSessionRecordingResponse | V2ErrorModel | None:
    r"""Get a session's screen recording URL

     Returns a short-lived URL for the session's screen recording, keyed on session_id — so it works for
    workflow runs and workflow-less interactive leases alike. Status is \"pending\" (no URL) when the
    recording hasn't finished uploading yet. Org-scoped: another org's session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSessionRecordingResponse | V2ErrorModel
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PhoneSessionRecordingResponse | V2ErrorModel]:
    r"""Get a session's screen recording URL

     Returns a short-lived URL for the session's screen recording, keyed on session_id — so it works for
    workflow runs and workflow-less interactive leases alike. Status is \"pending\" (no URL) when the
    recording hasn't finished uploading yet. Org-scoped: another org's session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSessionRecordingResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> PhoneSessionRecordingResponse | V2ErrorModel | None:
    r"""Get a session's screen recording URL

     Returns a short-lived URL for the session's screen recording, keyed on session_id — so it works for
    workflow runs and workflow-less interactive leases alike. Status is \"pending\" (no URL) when the
    recording hasn't finished uploading yet. Org-scoped: another org's session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSessionRecordingResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
