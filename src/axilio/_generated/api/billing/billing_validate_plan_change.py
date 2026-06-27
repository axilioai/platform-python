from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.subscription_downgrade_validation import SubscriptionDowngradeValidation
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response


def _get_kwargs(
    *,
    plan_id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["plan_id"] = plan_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/subscription/plan-change/validate",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SubscriptionDowngradeValidation | V2ErrorModel:
    if response.status_code == 200:
        response_200 = SubscriptionDowngradeValidation.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SubscriptionDowngradeValidation | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    plan_id: str,
) -> Response[SubscriptionDowngradeValidation | V2ErrorModel]:
    """Validate a plan change before executing

     Computes the impact (limit changes, blockers, warnings, effective date) of switching to plan_id.
    Admin only.

    Args:
        plan_id (str): target billing plan ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDowngradeValidation | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    plan_id: str,
) -> SubscriptionDowngradeValidation | V2ErrorModel | None:
    """Validate a plan change before executing

     Computes the impact (limit changes, blockers, warnings, effective date) of switching to plan_id.
    Admin only.

    Args:
        plan_id (str): target billing plan ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionDowngradeValidation | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        plan_id=plan_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    plan_id: str,
) -> Response[SubscriptionDowngradeValidation | V2ErrorModel]:
    """Validate a plan change before executing

     Computes the impact (limit changes, blockers, warnings, effective date) of switching to plan_id.
    Admin only.

    Args:
        plan_id (str): target billing plan ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDowngradeValidation | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        plan_id=plan_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    plan_id: str,
) -> SubscriptionDowngradeValidation | V2ErrorModel | None:
    """Validate a plan change before executing

     Computes the impact (limit changes, blockers, warnings, effective date) of switching to plan_id.
    Admin only.

    Args:
        plan_id (str): target billing plan ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionDowngradeValidation | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            plan_id=plan_id,
        )
    ).parsed
