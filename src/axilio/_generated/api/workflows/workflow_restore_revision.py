from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.v2_error_model import V2ErrorModel
from ...models.workflow_restore_revision_request import WorkflowRestoreRevisionRequest
from ...models.workflow_save_code_response import WorkflowSaveCodeResponse
from ...types import Response


def _get_kwargs(
    workflow_id: str,
    *,
    body: WorkflowRestoreRevisionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/workflows/{workflow_id}/code/restore".format(
            workflow_id=quote(str(workflow_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> V2ErrorModel | WorkflowSaveCodeResponse:
    if response.status_code == 200:
        response_200 = WorkflowSaveCodeResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[V2ErrorModel | WorkflowSaveCodeResponse]:
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
    body: WorkflowRestoreRevisionRequest,
) -> Response[V2ErrorModel | WorkflowSaveCodeResponse]:
    """Restore a workflow revision

     Creates a new revision with the source of the named revision. Does NOT dedup against the current
    revision so the action is auditable in the revision history.

    Args:
        workflow_id (str): workflow identifier
        body (WorkflowRestoreRevisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowSaveCodeResponse]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workflow_id: str,
    *,
    client: AuthenticatedClient,
    body: WorkflowRestoreRevisionRequest,
) -> V2ErrorModel | WorkflowSaveCodeResponse | None:
    """Restore a workflow revision

     Creates a new revision with the source of the named revision. Does NOT dedup against the current
    revision so the action is auditable in the revision history.

    Args:
        workflow_id (str): workflow identifier
        body (WorkflowRestoreRevisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowSaveCodeResponse
    """

    return sync_detailed(
        workflow_id=workflow_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workflow_id: str,
    *,
    client: AuthenticatedClient,
    body: WorkflowRestoreRevisionRequest,
) -> Response[V2ErrorModel | WorkflowSaveCodeResponse]:
    """Restore a workflow revision

     Creates a new revision with the source of the named revision. Does NOT dedup against the current
    revision so the action is auditable in the revision history.

    Args:
        workflow_id (str): workflow identifier
        body (WorkflowRestoreRevisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V2ErrorModel | WorkflowSaveCodeResponse]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workflow_id: str,
    *,
    client: AuthenticatedClient,
    body: WorkflowRestoreRevisionRequest,
) -> V2ErrorModel | WorkflowSaveCodeResponse | None:
    """Restore a workflow revision

     Creates a new revision with the source of the named revision. Does NOT dedup against the current
    revision so the action is auditable in the revision history.

    Args:
        workflow_id (str): workflow identifier
        body (WorkflowRestoreRevisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V2ErrorModel | WorkflowSaveCodeResponse
    """

    return (
        await asyncio_detailed(
            workflow_id=workflow_id,
            client=client,
            body=body,
        )
    ).parsed
