from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.v2_error_model import V2ErrorModel
from ...models.workflow_workflow_list_response import WorkflowWorkflowListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    platform: list[str] | None | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    last_run_after: str | Unset = UNSET,
    last_run_before: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["search"] = search

    json_status: list[str] | None | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, list):
        json_status = status

    else:
        json_status = status
    params["status"] = json_status

    json_platform: list[str] | None | Unset
    if isinstance(platform, Unset):
        json_platform = UNSET
    elif isinstance(platform, list):
        json_platform = platform

    else:
        json_platform = platform
    params["platform"] = json_platform

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["last_run_after"] = last_run_after

    params["last_run_before"] = last_run_before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workflows",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> V2ErrorModel | WorkflowWorkflowListResponse:
    if response.status_code == 200:
        response_200 = WorkflowWorkflowListResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[V2ErrorModel | WorkflowWorkflowListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    platform: list[str] | None | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    last_run_after: str | Unset = UNSET,
    last_run_before: str | Unset = UNSET,
) -> Response[V2ErrorModel | WorkflowWorkflowListResponse]:
    """List workflows (query params)

     Paginated list of workflows in the caller's org. Filters via query params: search, status, platform.
    Use POST /workflows/list for richer body-shaped queries with sort.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across workflow name
        status (list[str] | None | Unset): filter by workflow status (lowercase)
        platform (list[str] | None | Unset): filter by device platform (lowercase)
        created_after (str | Unset): only workflows created at/after this RFC3339 time
        created_before (str | Unset): only workflows created at/before this RFC3339 time
        last_run_after (str | Unset): only workflows last run at/after this RFC3339 time
        last_run_before (str | Unset): only workflows last run at/before this RFC3339 time

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowWorkflowListResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        status=status,
        platform=platform,
        created_after=created_after,
        created_before=created_before,
        last_run_after=last_run_after,
        last_run_before=last_run_before,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    platform: list[str] | None | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    last_run_after: str | Unset = UNSET,
    last_run_before: str | Unset = UNSET,
) -> V2ErrorModel | WorkflowWorkflowListResponse | None:
    """List workflows (query params)

     Paginated list of workflows in the caller's org. Filters via query params: search, status, platform.
    Use POST /workflows/list for richer body-shaped queries with sort.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across workflow name
        status (list[str] | None | Unset): filter by workflow status (lowercase)
        platform (list[str] | None | Unset): filter by device platform (lowercase)
        created_after (str | Unset): only workflows created at/after this RFC3339 time
        created_before (str | Unset): only workflows created at/before this RFC3339 time
        last_run_after (str | Unset): only workflows last run at/after this RFC3339 time
        last_run_before (str | Unset): only workflows last run at/before this RFC3339 time

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowWorkflowListResponse
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        search=search,
        status=status,
        platform=platform,
        created_after=created_after,
        created_before=created_before,
        last_run_after=last_run_after,
        last_run_before=last_run_before,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    platform: list[str] | None | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    last_run_after: str | Unset = UNSET,
    last_run_before: str | Unset = UNSET,
) -> Response[V2ErrorModel | WorkflowWorkflowListResponse]:
    """List workflows (query params)

     Paginated list of workflows in the caller's org. Filters via query params: search, status, platform.
    Use POST /workflows/list for richer body-shaped queries with sort.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across workflow name
        status (list[str] | None | Unset): filter by workflow status (lowercase)
        platform (list[str] | None | Unset): filter by device platform (lowercase)
        created_after (str | Unset): only workflows created at/after this RFC3339 time
        created_before (str | Unset): only workflows created at/before this RFC3339 time
        last_run_after (str | Unset): only workflows last run at/after this RFC3339 time
        last_run_before (str | Unset): only workflows last run at/before this RFC3339 time

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowWorkflowListResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        status=status,
        platform=platform,
        created_after=created_after,
        created_before=created_before,
        last_run_after=last_run_after,
        last_run_before=last_run_before,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    platform: list[str] | None | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    last_run_after: str | Unset = UNSET,
    last_run_before: str | Unset = UNSET,
) -> V2ErrorModel | WorkflowWorkflowListResponse | None:
    """List workflows (query params)

     Paginated list of workflows in the caller's org. Filters via query params: search, status, platform.
    Use POST /workflows/list for richer body-shaped queries with sort.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across workflow name
        status (list[str] | None | Unset): filter by workflow status (lowercase)
        platform (list[str] | None | Unset): filter by device platform (lowercase)
        created_after (str | Unset): only workflows created at/after this RFC3339 time
        created_before (str | Unset): only workflows created at/before this RFC3339 time
        last_run_after (str | Unset): only workflows last run at/after this RFC3339 time
        last_run_before (str | Unset): only workflows last run at/before this RFC3339 time

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowWorkflowListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            search=search,
            status=status,
            platform=platform,
            created_after=created_after,
            created_before=created_before,
            last_run_after=last_run_after,
            last_run_before=last_run_before,
        )
    ).parsed
