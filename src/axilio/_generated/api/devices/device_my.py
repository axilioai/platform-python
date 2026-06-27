from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.phone_private_phones_response import PhonePrivatePhonesResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_expired: bool | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    type_: list[str] | None | Unset = UNSET,
    rental_expires_after: str | Unset = UNSET,
    rental_expires_before: str | Unset = UNSET,
    last_active_after: str | Unset = UNSET,
    last_active_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_expired"] = include_expired

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

    json_type_: list[str] | None | Unset
    if isinstance(type_, Unset):
        json_type_ = UNSET
    elif isinstance(type_, list):
        json_type_ = type_

    else:
        json_type_ = type_
    params["type"] = json_type_

    params["rental_expires_after"] = rental_expires_after

    params["rental_expires_before"] = rental_expires_before

    params["last_active_after"] = last_active_after

    params["last_active_before"] = last_active_before

    params["sort"] = sort

    params["order"] = order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/phones/my",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PhonePrivatePhonesResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = PhonePrivatePhonesResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PhonePrivatePhonesResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    include_expired: bool | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    type_: list[str] | None | Unset = UNSET,
    rental_expires_after: str | Unset = UNSET,
    rental_expires_before: str | Unset = UNSET,
    last_active_after: str | Unset = UNSET,
    last_active_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> Response[PhonePrivatePhonesResponse | V2ErrorModel]:
    """List the caller's private + rented devices

     Returns private and rented devices owned by the caller's org. include_expired=true keeps rentals
    past their rental_expires_at in the result so users can see what they used to own.

    Args:
        include_expired (bool | Unset): include rented devices whose rental window has expired
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across nickname, name, model, location
        status (list[str] | None | Unset): filter by phone status
            (ACTIVE/INACTIVE/MAINTENANCE/SUSPENDED)
        type_ (list[str] | None | Unset): filter by phone type (IPHONE/ANDROID)
        rental_expires_after (str | Unset): only phones whose rental expires at/after this RFC3339
            time
        rental_expires_before (str | Unset): only phones whose rental expires at/before this
            RFC3339 time
        last_active_after (str | Unset): only phones last seen at/after this RFC3339 time
        last_active_before (str | Unset): only phones last seen at/before this RFC3339 time
        sort (str | Unset): sort column (created|rental_expires|last_active|status|type|location)
        order (str | Unset): sort direction (asc|desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhonePrivatePhonesResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        include_expired=include_expired,
        limit=limit,
        offset=offset,
        search=search,
        status=status,
        type_=type_,
        rental_expires_after=rental_expires_after,
        rental_expires_before=rental_expires_before,
        last_active_after=last_active_after,
        last_active_before=last_active_before,
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
    include_expired: bool | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    type_: list[str] | None | Unset = UNSET,
    rental_expires_after: str | Unset = UNSET,
    rental_expires_before: str | Unset = UNSET,
    last_active_after: str | Unset = UNSET,
    last_active_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> PhonePrivatePhonesResponse | V2ErrorModel | None:
    """List the caller's private + rented devices

     Returns private and rented devices owned by the caller's org. include_expired=true keeps rentals
    past their rental_expires_at in the result so users can see what they used to own.

    Args:
        include_expired (bool | Unset): include rented devices whose rental window has expired
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across nickname, name, model, location
        status (list[str] | None | Unset): filter by phone status
            (ACTIVE/INACTIVE/MAINTENANCE/SUSPENDED)
        type_ (list[str] | None | Unset): filter by phone type (IPHONE/ANDROID)
        rental_expires_after (str | Unset): only phones whose rental expires at/after this RFC3339
            time
        rental_expires_before (str | Unset): only phones whose rental expires at/before this
            RFC3339 time
        last_active_after (str | Unset): only phones last seen at/after this RFC3339 time
        last_active_before (str | Unset): only phones last seen at/before this RFC3339 time
        sort (str | Unset): sort column (created|rental_expires|last_active|status|type|location)
        order (str | Unset): sort direction (asc|desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhonePrivatePhonesResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        include_expired=include_expired,
        limit=limit,
        offset=offset,
        search=search,
        status=status,
        type_=type_,
        rental_expires_after=rental_expires_after,
        rental_expires_before=rental_expires_before,
        last_active_after=last_active_after,
        last_active_before=last_active_before,
        sort=sort,
        order=order,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    include_expired: bool | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    type_: list[str] | None | Unset = UNSET,
    rental_expires_after: str | Unset = UNSET,
    rental_expires_before: str | Unset = UNSET,
    last_active_after: str | Unset = UNSET,
    last_active_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> Response[PhonePrivatePhonesResponse | V2ErrorModel]:
    """List the caller's private + rented devices

     Returns private and rented devices owned by the caller's org. include_expired=true keeps rentals
    past their rental_expires_at in the result so users can see what they used to own.

    Args:
        include_expired (bool | Unset): include rented devices whose rental window has expired
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across nickname, name, model, location
        status (list[str] | None | Unset): filter by phone status
            (ACTIVE/INACTIVE/MAINTENANCE/SUSPENDED)
        type_ (list[str] | None | Unset): filter by phone type (IPHONE/ANDROID)
        rental_expires_after (str | Unset): only phones whose rental expires at/after this RFC3339
            time
        rental_expires_before (str | Unset): only phones whose rental expires at/before this
            RFC3339 time
        last_active_after (str | Unset): only phones last seen at/after this RFC3339 time
        last_active_before (str | Unset): only phones last seen at/before this RFC3339 time
        sort (str | Unset): sort column (created|rental_expires|last_active|status|type|location)
        order (str | Unset): sort direction (asc|desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PhonePrivatePhonesResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        include_expired=include_expired,
        limit=limit,
        offset=offset,
        search=search,
        status=status,
        type_=type_,
        rental_expires_after=rental_expires_after,
        rental_expires_before=rental_expires_before,
        last_active_after=last_active_after,
        last_active_before=last_active_before,
        sort=sort,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    include_expired: bool | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    status: list[str] | None | Unset = UNSET,
    type_: list[str] | None | Unset = UNSET,
    rental_expires_after: str | Unset = UNSET,
    rental_expires_before: str | Unset = UNSET,
    last_active_after: str | Unset = UNSET,
    last_active_before: str | Unset = UNSET,
    sort: str | Unset = UNSET,
    order: str | Unset = UNSET,
) -> PhonePrivatePhonesResponse | V2ErrorModel | None:
    """List the caller's private + rented devices

     Returns private and rented devices owned by the caller's org. include_expired=true keeps rentals
    past their rental_expires_at in the result so users can see what they used to own.

    Args:
        include_expired (bool | Unset): include rented devices whose rental window has expired
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        search (str | Unset): free-text search across nickname, name, model, location
        status (list[str] | None | Unset): filter by phone status
            (ACTIVE/INACTIVE/MAINTENANCE/SUSPENDED)
        type_ (list[str] | None | Unset): filter by phone type (IPHONE/ANDROID)
        rental_expires_after (str | Unset): only phones whose rental expires at/after this RFC3339
            time
        rental_expires_before (str | Unset): only phones whose rental expires at/before this
            RFC3339 time
        last_active_after (str | Unset): only phones last seen at/after this RFC3339 time
        last_active_before (str | Unset): only phones last seen at/before this RFC3339 time
        sort (str | Unset): sort column (created|rental_expires|last_active|status|type|location)
        order (str | Unset): sort direction (asc|desc)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PhonePrivatePhonesResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            include_expired=include_expired,
            limit=limit,
            offset=offset,
            search=search,
            status=status,
            type_=type_,
            rental_expires_after=rental_expires_after,
            rental_expires_before=rental_expires_before,
            last_active_after=last_active_after,
            last_active_before=last_active_before,
            sort=sort,
            order=order,
        )
    ).parsed
