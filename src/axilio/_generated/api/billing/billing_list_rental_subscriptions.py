from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_rental_phone_rental_subscription_list_response import (
    PhoneRentalPhoneRentalSubscriptionListResponse,
)
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 25,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    interval: str | Unset = UNSET,
    lifecycle: str | Unset = UNSET,
    payment: str | Unset = UNSET,
    renews_before: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["search"] = search

    params["interval"] = interval

    params["lifecycle"] = lifecycle

    params["payment"] = payment

    params["renews_before"] = renews_before

    params["sort_by"] = sort_by

    params["sort_order"] = sort_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/phone-rental-subscriptions/list",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhoneRentalPhoneRentalSubscriptionListResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 25,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    interval: str | Unset = UNSET,
    lifecycle: str | Unset = UNSET,
    payment: str | Unset = UNSET,
    renews_before: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
) -> Response[PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel]:
    """List active device rental subscriptions (paginated)

     Returns one filtered, sorted page of the caller organization's active device rental subscriptions,
    plus an org-wide summary (active count, combined monthly spend, per-interval breakdown, and upcoming
    charges).

    Args:
        limit (int | Unset): max items per page Default: 25.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across phone name/nickname
        interval (str | Unset): plan interval filter: day|week|month
        lifecycle (str | Unset): renewing|canceling (maps to cancel_at_period_end)
        payment (str | Unset): healthy|past_due
        renews_before (str | Unset): RFC3339 upper bound on current_period_end
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        interval=interval,
        lifecycle=lifecycle,
        payment=payment,
        renews_before=renews_before,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 25,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    interval: str | Unset = UNSET,
    lifecycle: str | Unset = UNSET,
    payment: str | Unset = UNSET,
    renews_before: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
) -> PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel | None:
    """List active device rental subscriptions (paginated)

     Returns one filtered, sorted page of the caller organization's active device rental subscriptions,
    plus an org-wide summary (active count, combined monthly spend, per-interval breakdown, and upcoming
    charges).

    Args:
        limit (int | Unset): max items per page Default: 25.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across phone name/nickname
        interval (str | Unset): plan interval filter: day|week|month
        lifecycle (str | Unset): renewing|canceling (maps to cancel_at_period_end)
        payment (str | Unset): healthy|past_due
        renews_before (str | Unset): RFC3339 upper bound on current_period_end
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        search=search,
        interval=interval,
        lifecycle=lifecycle,
        payment=payment,
        renews_before=renews_before,
        sort_by=sort_by,
        sort_order=sort_order,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 25,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    interval: str | Unset = UNSET,
    lifecycle: str | Unset = UNSET,
    payment: str | Unset = UNSET,
    renews_before: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
) -> Response[PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel]:
    """List active device rental subscriptions (paginated)

     Returns one filtered, sorted page of the caller organization's active device rental subscriptions,
    plus an org-wide summary (active count, combined monthly spend, per-interval breakdown, and upcoming
    charges).

    Args:
        limit (int | Unset): max items per page Default: 25.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across phone name/nickname
        interval (str | Unset): plan interval filter: day|week|month
        lifecycle (str | Unset): renewing|canceling (maps to cancel_at_period_end)
        payment (str | Unset): healthy|past_due
        renews_before (str | Unset): RFC3339 upper bound on current_period_end
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        search=search,
        interval=interval,
        lifecycle=lifecycle,
        payment=payment,
        renews_before=renews_before,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 25,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    interval: str | Unset = UNSET,
    lifecycle: str | Unset = UNSET,
    payment: str | Unset = UNSET,
    renews_before: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,
) -> PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel | None:
    """List active device rental subscriptions (paginated)

     Returns one filtered, sorted page of the caller organization's active device rental subscriptions,
    plus an org-wide summary (active count, combined monthly spend, per-interval breakdown, and upcoming
    charges).

    Args:
        limit (int | Unset): max items per page Default: 25.
        offset (int | Unset): pagination offset Default: 0.
        search (str | Unset): free-text search across phone name/nickname
        interval (str | Unset): plan interval filter: day|week|month
        lifecycle (str | Unset): renewing|canceling (maps to cancel_at_period_end)
        payment (str | Unset): healthy|past_due
        renews_before (str | Unset): RFC3339 upper bound on current_period_end
        sort_by (str | Unset): column to sort by
        sort_order (str | Unset): asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhoneRentalPhoneRentalSubscriptionListResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            search=search,
            interval=interval,
            lifecycle=lifecycle,
            payment=payment,
            renews_before=renews_before,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    ).parsed
