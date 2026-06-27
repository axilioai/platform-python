from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.v2_error_model import V2ErrorModel
from ...models.workflow_workflow_create_request import WorkflowWorkflowCreateRequest
from ...models.workflow_workflow_create_response import WorkflowWorkflowCreateResponse
from ...types import Response


def _get_kwargs(
    *,
    body: WorkflowWorkflowCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/workflows",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> V2ErrorModel | WorkflowWorkflowCreateResponse:
    if response.status_code == 201:
        response_201 = WorkflowWorkflowCreateResponse.from_dict(response.json())

        return response_201

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[V2ErrorModel | WorkflowWorkflowCreateResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: WorkflowWorkflowCreateRequest,
) -> Response[V2ErrorModel | WorkflowWorkflowCreateResponse]:
    """Create a workflow

     Creates a new workflow in the caller's org. Name must match ^[A-Za-z0-9_-]+$ and be unique within
    the org. Returns the workflow_id.

    Args:
        body (WorkflowWorkflowCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowWorkflowCreateResponse]
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
    body: WorkflowWorkflowCreateRequest,
) -> V2ErrorModel | WorkflowWorkflowCreateResponse | None:
    """Create a workflow

     Creates a new workflow in the caller's org. Name must match ^[A-Za-z0-9_-]+$ and be unique within
    the org. Returns the workflow_id.

    Args:
        body (WorkflowWorkflowCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowWorkflowCreateResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: WorkflowWorkflowCreateRequest,
) -> Response[V2ErrorModel | WorkflowWorkflowCreateResponse]:
    """Create a workflow

     Creates a new workflow in the caller's org. Name must match ^[A-Za-z0-9_-]+$ and be unique within
    the org. Returns the workflow_id.

    Args:
        body (WorkflowWorkflowCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowWorkflowCreateResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: WorkflowWorkflowCreateRequest,
) -> V2ErrorModel | WorkflowWorkflowCreateResponse | None:
    """Create a workflow

     Creates a new workflow in the caller's org. Name must match ^[A-Za-z0-9_-]+$ and be unique within
    the org. Returns the workflow_id.

    Args:
        body (WorkflowWorkflowCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowWorkflowCreateResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
