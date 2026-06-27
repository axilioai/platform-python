from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_allocation_status_response import PhoneAllocationStatusResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workflow_id: str,
    allocated_by: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["workflow_id"] = workflow_id

    params["allocated_by"] = allocated_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/allocation-status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneAllocationStatusResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneAllocationStatusResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneAllocationStatusResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    allocated_by: str | Unset = UNSET,
) -> Response[PhoneAllocationStatusResponse | V2ErrorModel]:
    """Check if a workflow has an active device

     Returns whether the given workflow currently holds an active device allocation, including the
    session_id when present. The optional allocated_by filter narrows results to allocations originating
    from a specific context (workflow_editor / scheduler).

    Args:
        workflow_id (str): workflow identifier
        allocated_by (str | Unset): optional: only consider allocations made via this context
            (workflow_editor/scheduler)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneAllocationStatusResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        allocated_by=allocated_by,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    allocated_by: str | Unset = UNSET,
) -> PhoneAllocationStatusResponse | V2ErrorModel | None:
    """Check if a workflow has an active device

     Returns whether the given workflow currently holds an active device allocation, including the
    session_id when present. The optional allocated_by filter narrows results to allocations originating
    from a specific context (workflow_editor / scheduler).

    Args:
        workflow_id (str): workflow identifier
        allocated_by (str | Unset): optional: only consider allocations made via this context
            (workflow_editor/scheduler)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneAllocationStatusResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        workflow_id=workflow_id,
        allocated_by=allocated_by,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    allocated_by: str | Unset = UNSET,
) -> Response[PhoneAllocationStatusResponse | V2ErrorModel]:
    """Check if a workflow has an active device

     Returns whether the given workflow currently holds an active device allocation, including the
    session_id when present. The optional allocated_by filter narrows results to allocations originating
    from a specific context (workflow_editor / scheduler).

    Args:
        workflow_id (str): workflow identifier
        allocated_by (str | Unset): optional: only consider allocations made via this context
            (workflow_editor/scheduler)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneAllocationStatusResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        allocated_by=allocated_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    workflow_id: str,
    allocated_by: str | Unset = UNSET,
) -> PhoneAllocationStatusResponse | V2ErrorModel | None:
    """Check if a workflow has an active device

     Returns whether the given workflow currently holds an active device allocation, including the
    session_id when present. The optional allocated_by filter narrows results to allocations originating
    from a specific context (workflow_editor / scheduler).

    Args:
        workflow_id (str): workflow identifier
        allocated_by (str | Unset): optional: only consider allocations made via this context
            (workflow_editor/scheduler)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneAllocationStatusResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            workflow_id=workflow_id,
            allocated_by=allocated_by,
        )
    ).parsed
