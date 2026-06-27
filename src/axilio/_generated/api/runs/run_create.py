from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.run_run_create_request import RunRunCreateRequest
from ...models.run_run_create_response import RunRunCreateResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs(
    workflow_id: str,
    *,
    body: RunRunCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/runs/{workflow_id}".format(
            workflow_id=quote(str(workflow_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RunRunCreateResponse | V2ErrorModel:
    if response.status_code == 201:
        response_201 = RunRunCreateResponse.from_dict(response.json())

        return response_201

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RunRunCreateResponse | V2ErrorModel]:
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
    body: RunRunCreateRequest,
) -> Response[RunRunCreateResponse | V2ErrorModel]:
    """Start one or more runs

     Creates one or more runs against the given workflow and queues them for execution. Pre-flight
    checks: balance sufficient, concurrency limit, workflow exists. Runs that fail to queue are marked
    FAILED immediately so they stop counting toward the concurrency limit.

    Args:
        workflow_id (str): workflow to create runs for
        body (RunRunCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunRunCreateResponse | V2ErrorModel]
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
    body: RunRunCreateRequest,
) -> RunRunCreateResponse | V2ErrorModel | None:
    """Start one or more runs

     Creates one or more runs against the given workflow and queues them for execution. Pre-flight
    checks: balance sufficient, concurrency limit, workflow exists. Runs that fail to queue are marked
    FAILED immediately so they stop counting toward the concurrency limit.

    Args:
        workflow_id (str): workflow to create runs for
        body (RunRunCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunRunCreateResponse | V2ErrorModel
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
    body: RunRunCreateRequest,
) -> Response[RunRunCreateResponse | V2ErrorModel]:
    """Start one or more runs

     Creates one or more runs against the given workflow and queues them for execution. Pre-flight
    checks: balance sufficient, concurrency limit, workflow exists. Runs that fail to queue are marked
    FAILED immediately so they stop counting toward the concurrency limit.

    Args:
        workflow_id (str): workflow to create runs for
        body (RunRunCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunRunCreateResponse | V2ErrorModel]
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
    body: RunRunCreateRequest,
) -> RunRunCreateResponse | V2ErrorModel | None:
    """Start one or more runs

     Creates one or more runs against the given workflow and queues them for execution. Pre-flight
    checks: balance sufficient, concurrency limit, workflow exists. Runs that fail to queue are marked
    FAILED immediately so they stop counting toward the concurrency limit.

    Args:
        workflow_id (str): workflow to create runs for
        body (RunRunCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunRunCreateResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            workflow_id=workflow_id,
            client=client,
            body=body,
        )
    ).parsed
