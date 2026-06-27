from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.billing_history_billing_history_response import BillingHistoryBillingHistoryResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    billing_cycle: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
    status: str | Unset = UNSET,
    date_from: str | Unset = UNSET,
    date_to: str | Unset = UNSET,
    plan_name: str | Unset = UNSET,
    phone_id: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["search"] = search

    params["billing_cycle"] = billing_cycle

    params["sort_by"] = sort_by

    params["sort_order"] = sort_order

    params["status"] = status

    params["date_from"] = date_from

    params["date_to"] = date_to

    params["plan_name"] = plan_name

    params["phone_id"] = phone_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/history",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BillingHistoryBillingHistoryResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = BillingHistoryBillingHistoryResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BillingHistoryBillingHistoryResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    billing_cycle: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
    status: str | Unset = UNSET,
    date_from: str | Unset = UNSET,
    date_to: str | Unset = UNSET,
    plan_name: str | Unset = UNSET,
    phone_id: str | Unset = UNSET,
) -> Response[BillingHistoryBillingHistoryResponse | V2ErrorModel]:
    """List billing history

     Paginated invoice history for the caller's organization with optional filters and sort.

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across invoice number/description
        billing_cycle (str | Unset): filter by billing cycle
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc
        status (str | Unset): invoice status filter (lowercase)
        date_from (str | Unset): RFC3339 lower bound for invoice_date
        date_to (str | Unset): RFC3339 upper bound for invoice_date (with date_from = an exact
            calendar month)
        plan_name (str | Unset): filter by plan name
        phone_id (str | Unset): filter to invoices for a dedicated phone

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BillingHistoryBillingHistoryResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        billing_cycle=billing_cycle,
        sort_by=sort_by,
        sort_order=sort_order,
        status=status,
        date_from=date_from,
        date_to=date_to,
        plan_name=plan_name,
        phone_id=phone_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    billing_cycle: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
    status: str | Unset = UNSET,
    date_from: str | Unset = UNSET,
    date_to: str | Unset = UNSET,
    plan_name: str | Unset = UNSET,
    phone_id: str | Unset = UNSET,
) -> BillingHistoryBillingHistoryResponse | V2ErrorModel | None:
    """List billing history

     Paginated invoice history for the caller's organization with optional filters and sort.

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across invoice number/description
        billing_cycle (str | Unset): filter by billing cycle
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc
        status (str | Unset): invoice status filter (lowercase)
        date_from (str | Unset): RFC3339 lower bound for invoice_date
        date_to (str | Unset): RFC3339 upper bound for invoice_date (with date_from = an exact
            calendar month)
        plan_name (str | Unset): filter by plan name
        phone_id (str | Unset): filter to invoices for a dedicated phone

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BillingHistoryBillingHistoryResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        search=search,
        billing_cycle=billing_cycle,
        sort_by=sort_by,
        sort_order=sort_order,
        status=status,
        date_from=date_from,
        date_to=date_to,
        plan_name=plan_name,
        phone_id=phone_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    billing_cycle: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
    status: str | Unset = UNSET,
    date_from: str | Unset = UNSET,
    date_to: str | Unset = UNSET,
    plan_name: str | Unset = UNSET,
    phone_id: str | Unset = UNSET,
) -> Response[BillingHistoryBillingHistoryResponse | V2ErrorModel]:
    """List billing history

     Paginated invoice history for the caller's organization with optional filters and sort.

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across invoice number/description
        billing_cycle (str | Unset): filter by billing cycle
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc
        status (str | Unset): invoice status filter (lowercase)
        date_from (str | Unset): RFC3339 lower bound for invoice_date
        date_to (str | Unset): RFC3339 upper bound for invoice_date (with date_from = an exact
            calendar month)
        plan_name (str | Unset): filter by plan name
        phone_id (str | Unset): filter to invoices for a dedicated phone

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BillingHistoryBillingHistoryResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        billing_cycle=billing_cycle,
        sort_by=sort_by,
        sort_order=sort_order,
        status=status,
        date_from=date_from,
        date_to=date_to,
        plan_name=plan_name,
        phone_id=phone_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    billing_cycle: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
    status: str | Unset = UNSET,
    date_from: str | Unset = UNSET,
    date_to: str | Unset = UNSET,
    plan_name: str | Unset = UNSET,
    phone_id: str | Unset = UNSET,
) -> BillingHistoryBillingHistoryResponse | V2ErrorModel | None:
    """List billing history

     Paginated invoice history for the caller's organization with optional filters and sort.

    Args:
        limit (int | Unset): max items per page Default: 50.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across invoice number/description
        billing_cycle (str | Unset): filter by billing cycle
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc
        status (str | Unset): invoice status filter (lowercase)
        date_from (str | Unset): RFC3339 lower bound for invoice_date
        date_to (str | Unset): RFC3339 upper bound for invoice_date (with date_from = an exact
            calendar month)
        plan_name (str | Unset): filter by plan name
        phone_id (str | Unset): filter to invoices for a dedicated phone

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BillingHistoryBillingHistoryResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            search=search,
            billing_cycle=billing_cycle,
            sort_by=sort_by,
            sort_order=sort_order,
            status=status,
            date_from=date_from,
            date_to=date_to,
            plan_name=plan_name,
            phone_id=phone_id,
        )
    ).parsed
