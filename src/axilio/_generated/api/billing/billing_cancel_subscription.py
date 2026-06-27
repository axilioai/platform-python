from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.subscription_cancel_subscription_response import SubscriptionCancelSubscriptionResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/billing/subscription/cancel",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SubscriptionCancelSubscriptionResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = SubscriptionCancelSubscriptionResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SubscriptionCancelSubscriptionResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[SubscriptionCancelSubscriptionResponse | V2ErrorModel]:
    """Cancel subscription at period end

     Marks the active subscription to cancel at the end of the current billing period. Admin only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionCancelSubscriptionResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> SubscriptionCancelSubscriptionResponse | V2ErrorModel | None:
    """Cancel subscription at period end

     Marks the active subscription to cancel at the end of the current billing period. Admin only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionCancelSubscriptionResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[SubscriptionCancelSubscriptionResponse | V2ErrorModel]:
    """Cancel subscription at period end

     Marks the active subscription to cancel at the end of the current billing period. Admin only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionCancelSubscriptionResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> SubscriptionCancelSubscriptionResponse | V2ErrorModel | None:
    """Cancel subscription at period end

     Marks the active subscription to cancel at the end of the current billing period. Admin only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionCancelSubscriptionResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
