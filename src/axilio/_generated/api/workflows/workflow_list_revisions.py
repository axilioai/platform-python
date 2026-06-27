from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.v2_error_model import V2ErrorModel
from ...models.workflow_list_revisions_response import WorkflowListRevisionsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workflow_id: str,
    *,
    limit: int | Unset = 50,
    before: int | Unset = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["before"] = before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workflows/{workflow_id}/revisions".format(
            workflow_id=quote(str(workflow_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> V2ErrorModel | WorkflowListRevisionsResponse:
    if response.status_code == 200:
        response_200 = WorkflowListRevisionsResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[V2ErrorModel | WorkflowListRevisionsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workflow_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    before: int | Unset = 0,
) -> Response[V2ErrorModel | WorkflowListRevisionsResponse]:
    """List workflow revisions

     Returns revision metadata (id, number, author, message, bytes, sha256, created_at) for the workflow,
    in reverse-chronological order. Use the `before` cursor to paginate older revisions.

    Args:
        workflow_id (str): workflow identifier
        limit (int | Unset):  Default: 50.
        before (int | Unset): cursor: return revisions older than this revision number Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowListRevisionsResponse]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        limit=limit,
        before=before,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workflow_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    before: int | Unset = 0,
) -> V2ErrorModel | WorkflowListRevisionsResponse | None:
    """List workflow revisions

     Returns revision metadata (id, number, author, message, bytes, sha256, created_at) for the workflow,
    in reverse-chronological order. Use the `before` cursor to paginate older revisions.

    Args:
        workflow_id (str): workflow identifier
        limit (int | Unset):  Default: 50.
        before (int | Unset): cursor: return revisions older than this revision number Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowListRevisionsResponse
    """

    return sync_detailed(
        workflow_id=workflow_id,
        client=client,
        limit=limit,
        before=before,
    ).parsed


async def asyncio_detailed(
    workflow_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    before: int | Unset = 0,
) -> Response[V2ErrorModel | WorkflowListRevisionsResponse]:
    """List workflow revisions

     Returns revision metadata (id, number, author, message, bytes, sha256, created_at) for the workflow,
    in reverse-chronological order. Use the `before` cursor to paginate older revisions.

    Args:
        workflow_id (str): workflow identifier
        limit (int | Unset):  Default: 50.
        before (int | Unset): cursor: return revisions older than this revision number Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowListRevisionsResponse]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        limit=limit,
        before=before,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workflow_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    before: int | Unset = 0,
) -> V2ErrorModel | WorkflowListRevisionsResponse | None:
    """List workflow revisions

     Returns revision metadata (id, number, author, message, bytes, sha256, created_at) for the workflow,
    in reverse-chronological order. Use the `before` cursor to paginate older revisions.

    Args:
        workflow_id (str): workflow identifier
        limit (int | Unset):  Default: 50.
        before (int | Unset): cursor: return revisions older than this revision number Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowListRevisionsResponse
    """

    return (
        await asyncio_detailed(
            workflow_id=workflow_id,
            client=client,
            limit=limit,
            before=before,
        )
    ).parsed
