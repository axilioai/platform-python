from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_active_sessions_response import PhoneActiveSessionsResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    dedicated: str | Unset = UNSET,
    source: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["search"] = search

    params["dedicated"] = dedicated

    params["source"] = source

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/sessions/active",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneActiveSessionsResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneActiveSessionsResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneActiveSessionsResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    dedicated: str | Unset = UNSET,
    source: str | Unset = UNSET,
) -> Response[PhoneActiveSessionsResponse | V2ErrorModel]:
    """List the org's active phone allocations

     Returns one page of the organization's currently-active phone sessions joined with phone + workflow
    display fields: in-flight runs, workflow-less interactive leases, and dedicated phones in use.
    Paginated via limit (default 25, max 100) + offset; the response total is the full active count.
    Powers the dashboard overview.

    Args:
        limit (int | Unset): max rows to return (default 25, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone name/nickname/id, session id, or
            workflow name
        dedicated (str | Unset): filter by ownership: 'dedicated' or 'shared'
        source (str | Unset): filter by source: 'workflow' or 'interactive'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneActiveSessionsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        dedicated=dedicated,
        source=source,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    dedicated: str | Unset = UNSET,
    source: str | Unset = UNSET,
) -> PhoneActiveSessionsResponse | V2ErrorModel | None:
    """List the org's active phone allocations

     Returns one page of the organization's currently-active phone sessions joined with phone + workflow
    display fields: in-flight runs, workflow-less interactive leases, and dedicated phones in use.
    Paginated via limit (default 25, max 100) + offset; the response total is the full active count.
    Powers the dashboard overview.

    Args:
        limit (int | Unset): max rows to return (default 25, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone name/nickname/id, session id, or
            workflow name
        dedicated (str | Unset): filter by ownership: 'dedicated' or 'shared'
        source (str | Unset): filter by source: 'workflow' or 'interactive'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneActiveSessionsResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        search=search,
        dedicated=dedicated,
        source=source,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    dedicated: str | Unset = UNSET,
    source: str | Unset = UNSET,
) -> Response[PhoneActiveSessionsResponse | V2ErrorModel]:
    """List the org's active phone allocations

     Returns one page of the organization's currently-active phone sessions joined with phone + workflow
    display fields: in-flight runs, workflow-less interactive leases, and dedicated phones in use.
    Paginated via limit (default 25, max 100) + offset; the response total is the full active count.
    Powers the dashboard overview.

    Args:
        limit (int | Unset): max rows to return (default 25, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone name/nickname/id, session id, or
            workflow name
        dedicated (str | Unset): filter by ownership: 'dedicated' or 'shared'
        source (str | Unset): filter by source: 'workflow' or 'interactive'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneActiveSessionsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        dedicated=dedicated,
        source=source,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    dedicated: str | Unset = UNSET,
    source: str | Unset = UNSET,
) -> PhoneActiveSessionsResponse | V2ErrorModel | None:
    """List the org's active phone allocations

     Returns one page of the organization's currently-active phone sessions joined with phone + workflow
    display fields: in-flight runs, workflow-less interactive leases, and dedicated phones in use.
    Paginated via limit (default 25, max 100) + offset; the response total is the full active count.
    Powers the dashboard overview.

    Args:
        limit (int | Unset): max rows to return (default 25, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone name/nickname/id, session id, or
            workflow name
        dedicated (str | Unset): filter by ownership: 'dedicated' or 'shared'
        source (str | Unset): filter by source: 'workflow' or 'interactive'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneActiveSessionsResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            search=search,
            dedicated=dedicated,
            source=source,
        )
    ).parsed
