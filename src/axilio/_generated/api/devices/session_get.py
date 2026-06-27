from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_session_detail_response import PhoneSessionDetailResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/sessions/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneSessionDetailResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneSessionDetailResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneSessionDetailResponse | V2ErrorModel]:
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
) -> Response[PhoneSessionDetailResponse | V2ErrorModel]:
    """Get a session's detail

     Returns one session for the Session Inspector: session lifecycle + phone display fields + workflow
    name (when tied to one) + an inlined presigned recording URL. Works for active and terminal
    sessions, and for workflow runs and workflow-less interactive leases. Org-scoped: another org's
    session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSessionDetailResponse | V2ErrorModel]
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
) -> PhoneSessionDetailResponse | V2ErrorModel | None:
    """Get a session's detail

     Returns one session for the Session Inspector: session lifecycle + phone display fields + workflow
    name (when tied to one) + an inlined presigned recording URL. Works for active and terminal
    sessions, and for workflow runs and workflow-less interactive leases. Org-scoped: another org's
    session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSessionDetailResponse | V2ErrorModel
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PhoneSessionDetailResponse | V2ErrorModel]:
    """Get a session's detail

     Returns one session for the Session Inspector: session lifecycle + phone display fields + workflow
    name (when tied to one) + an inlined presigned recording URL. Works for active and terminal
    sessions, and for workflow runs and workflow-less interactive leases. Org-scoped: another org's
    session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSessionDetailResponse | V2ErrorModel]
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
) -> PhoneSessionDetailResponse | V2ErrorModel | None:
    """Get a session's detail

     Returns one session for the Session Inspector: session lifecycle + phone display fields + workflow
    name (when tied to one) + an inlined presigned recording URL. Works for active and terminal
    sessions, and for workflow runs and workflow-less interactive leases. Org-scoped: another org's
    session reads as not found.

    Args:
        id (str): phone session id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSessionDetailResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
