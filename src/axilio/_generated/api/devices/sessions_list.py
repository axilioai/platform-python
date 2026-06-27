from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_sessions_list_response import PhoneSessionsListResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    workflow_id: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    source: list[str] | None | Unset = UNSET,
    dedicated: list[str] | None | Unset = UNSET,
    started_after: str | Unset = UNSET,
    started_before: str | Unset = UNSET,
    ended_after: str | Unset = UNSET,
    ended_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["search"] = search

    params["workflow_id"] = workflow_id

    json_status: list[str] | None | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, list):
        json_status = status

    else:
        json_status = status
    params["status"] = json_status

    json_source: list[str] | None | Unset
    if isinstance(source, Unset):
        json_source = UNSET
    elif isinstance(source, list):
        json_source = source

    else:
        json_source = source
    params["source"] = json_source

    json_dedicated: list[str] | None | Unset
    if isinstance(dedicated, Unset):
        json_dedicated = UNSET
    elif isinstance(dedicated, list):
        json_dedicated = dedicated

    else:
        json_dedicated = dedicated
    params["dedicated"] = json_dedicated

    params["started_after"] = started_after

    params["started_before"] = started_before

    params["ended_after"] = ended_after

    params["ended_before"] = ended_before

    params["sort"] = sort

    params["order"] = order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/sessions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneSessionsListResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneSessionsListResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneSessionsListResponse | V2ErrorModel]:
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
    workflow_id: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    source: list[str] | None | Unset = UNSET,
    dedicated: list[str] | None | Unset = UNSET,
    started_after: str | Unset = UNSET,
    started_before: str | Unset = UNSET,
    ended_after: str | Unset = UNSET,
    ended_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> Response[PhoneSessionsListResponse | V2ErrorModel]:
    """List the org's sessions (unified history)

     Returns one page of the org's phone sessions for the Session Inspector table: active/unbilled
    sessions pinned on top, terminal history paginated beneath. Covers workflow runs and workflow-less
    interactive leases; each row links to a session. Filters: search, workflow_id, status.

    Args:
        limit (int | Unset): max rows to return (default 50, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone/session/workflow
        workflow_id (str | Unset): only sessions for this workflow
        status (list[str] | None | Unset): filter by session status
            (ACTIVE/COMPLETED/CANCELLED/EXPIRED); repeatable
        source (list[str] | None | Unset): filter by source: workflow and/or interactive;
            repeatable
        dedicated (list[str] | None | Unset): filter by type: shared and/or dedicated; repeatable
        started_after (str | Unset): only sessions started at/after this RFC3339 time
        started_before (str | Unset): only sessions started at/before this RFC3339 time
        ended_after (str | Unset): only sessions de-allocated at/after this RFC3339 time
        ended_before (str | Unset): only sessions de-allocated at/before this RFC3339 time
        sort (str | Unset): sort column: started|ended|status|duration (default started)
        order (str | Unset): sort direction: asc|desc (default desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSessionsListResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        workflow_id=workflow_id,
        status=status,
        source=source,
        dedicated=dedicated,
        started_after=started_after,
        started_before=started_before,
        ended_after=ended_after,
        ended_before=ended_before,
        sort=sort,
        order=order,
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
    workflow_id: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    source: list[str] | None | Unset = UNSET,
    dedicated: list[str] | None | Unset = UNSET,
    started_after: str | Unset = UNSET,
    started_before: str | Unset = UNSET,
    ended_after: str | Unset = UNSET,
    ended_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> PhoneSessionsListResponse | V2ErrorModel | None:
    """List the org's sessions (unified history)

     Returns one page of the org's phone sessions for the Session Inspector table: active/unbilled
    sessions pinned on top, terminal history paginated beneath. Covers workflow runs and workflow-less
    interactive leases; each row links to a session. Filters: search, workflow_id, status.

    Args:
        limit (int | Unset): max rows to return (default 50, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone/session/workflow
        workflow_id (str | Unset): only sessions for this workflow
        status (list[str] | None | Unset): filter by session status
            (ACTIVE/COMPLETED/CANCELLED/EXPIRED); repeatable
        source (list[str] | None | Unset): filter by source: workflow and/or interactive;
            repeatable
        dedicated (list[str] | None | Unset): filter by type: shared and/or dedicated; repeatable
        started_after (str | Unset): only sessions started at/after this RFC3339 time
        started_before (str | Unset): only sessions started at/before this RFC3339 time
        ended_after (str | Unset): only sessions de-allocated at/after this RFC3339 time
        ended_before (str | Unset): only sessions de-allocated at/before this RFC3339 time
        sort (str | Unset): sort column: started|ended|status|duration (default started)
        order (str | Unset): sort direction: asc|desc (default desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSessionsListResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        search=search,
        workflow_id=workflow_id,
        status=status,
        source=source,
        dedicated=dedicated,
        started_after=started_after,
        started_before=started_before,
        ended_after=ended_after,
        ended_before=ended_before,
        sort=sort,
        order=order,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    workflow_id: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    source: list[str] | None | Unset = UNSET,
    dedicated: list[str] | None | Unset = UNSET,
    started_after: str | Unset = UNSET,
    started_before: str | Unset = UNSET,
    ended_after: str | Unset = UNSET,
    ended_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> Response[PhoneSessionsListResponse | V2ErrorModel]:
    """List the org's sessions (unified history)

     Returns one page of the org's phone sessions for the Session Inspector table: active/unbilled
    sessions pinned on top, terminal history paginated beneath. Covers workflow runs and workflow-less
    interactive leases; each row links to a session. Filters: search, workflow_id, status.

    Args:
        limit (int | Unset): max rows to return (default 50, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone/session/workflow
        workflow_id (str | Unset): only sessions for this workflow
        status (list[str] | None | Unset): filter by session status
            (ACTIVE/COMPLETED/CANCELLED/EXPIRED); repeatable
        source (list[str] | None | Unset): filter by source: workflow and/or interactive;
            repeatable
        dedicated (list[str] | None | Unset): filter by type: shared and/or dedicated; repeatable
        started_after (str | Unset): only sessions started at/after this RFC3339 time
        started_before (str | Unset): only sessions started at/before this RFC3339 time
        ended_after (str | Unset): only sessions de-allocated at/after this RFC3339 time
        ended_before (str | Unset): only sessions de-allocated at/before this RFC3339 time
        sort (str | Unset): sort column: started|ended|status|duration (default started)
        order (str | Unset): sort direction: asc|desc (default desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneSessionsListResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        workflow_id=workflow_id,
        status=status,
        source=source,
        dedicated=dedicated,
        started_after=started_after,
        started_before=started_before,
        ended_after=ended_after,
        ended_before=ended_before,
        sort=sort,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    search: str | Unset = UNSET,
    workflow_id: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    source: list[str] | None | Unset = UNSET,
    dedicated: list[str] | None | Unset = UNSET,
    started_after: str | Unset = UNSET,
    started_before: str | Unset = UNSET,
    ended_after: str | Unset = UNSET,
    ended_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> PhoneSessionsListResponse | V2ErrorModel | None:
    """List the org's sessions (unified history)

     Returns one page of the org's phone sessions for the Session Inspector table: active/unbilled
    sessions pinned on top, terminal history paginated beneath. Covers workflow runs and workflow-less
    interactive leases; each row links to a session. Filters: search, workflow_id, status.

    Args:
        limit (int | Unset): max rows to return (default 50, max 100)
        offset (int | Unset): rows to skip for pagination
        search (str | Unset): case-insensitive match on phone/session/workflow
        workflow_id (str | Unset): only sessions for this workflow
        status (list[str] | None | Unset): filter by session status
            (ACTIVE/COMPLETED/CANCELLED/EXPIRED); repeatable
        source (list[str] | None | Unset): filter by source: workflow and/or interactive;
            repeatable
        dedicated (list[str] | None | Unset): filter by type: shared and/or dedicated; repeatable
        started_after (str | Unset): only sessions started at/after this RFC3339 time
        started_before (str | Unset): only sessions started at/before this RFC3339 time
        ended_after (str | Unset): only sessions de-allocated at/after this RFC3339 time
        ended_before (str | Unset): only sessions de-allocated at/before this RFC3339 time
        sort (str | Unset): sort column: started|ended|status|duration (default started)
        order (str | Unset): sort direction: asc|desc (default desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneSessionsListResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            search=search,
            workflow_id=workflow_id,
            status=status,
            source=source,
            dedicated=dedicated,
            started_after=started_after,
            started_before=started_before,
            ended_after=ended_after,
            ended_before=ended_before,
            sort=sort,
            order=order,
        )
    ).parsed
