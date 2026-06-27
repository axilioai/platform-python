import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.usage_get_metrics_granularity import UsageGetMetricsGranularity
from ...models.usage_usage_metrics_response import UsageUsageMetricsResponse
from ...models.v2_error_model import V2ErrorModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    granularity: UsageGetMetricsGranularity | Unset = UsageGetMetricsGranularity.DAILY,
    timezone: str | Unset = "UTC",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    json_granularity: str | Unset = UNSET
    if not isinstance(granularity, Unset):
        json_granularity = granularity.value

    params["granularity"] = json_granularity

    params["timezone"] = timezone

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/usage/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> UsageUsageMetricsResponse | V2ErrorModel:
    if response.status_code == 200:
        response_200 = UsageUsageMetricsResponse.from_dict(response.json())

        return response_200

    response_default = V2ErrorModel.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[UsageUsageMetricsResponse | V2ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    granularity: UsageGetMetricsGranularity | Unset = UsageGetMetricsGranularity.DAILY,
    timezone: str | Unset = "UTC",
) -> Response[UsageUsageMetricsResponse | V2ErrorModel]:
    """Get usage metrics (simple)

     Returns infrastructure cost and compute-minute summaries for the caller's user over a date range,
    plus per-bucket chart data. Granularity is hourly (≤24h window) or daily. Use POST /usage/metrics if
    you need richer body params; this endpoint takes query params only.

    Args:
        start_date (datetime.datetime): start of reporting window (RFC3339)
        end_date (datetime.datetime): end of reporting window (RFC3339)
        granularity (UsageGetMetricsGranularity | Unset): bucket resolution Default:
            UsageGetMetricsGranularity.DAILY.
        timezone (str | Unset): IANA timezone for bucketing periods (e.g., America/Los_Angeles)
            Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsageUsageMetricsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        granularity=granularity,
        timezone=timezone,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    granularity: UsageGetMetricsGranularity | Unset = UsageGetMetricsGranularity.DAILY,
    timezone: str | Unset = "UTC",
) -> UsageUsageMetricsResponse | V2ErrorModel | None:
    """Get usage metrics (simple)

     Returns infrastructure cost and compute-minute summaries for the caller's user over a date range,
    plus per-bucket chart data. Granularity is hourly (≤24h window) or daily. Use POST /usage/metrics if
    you need richer body params; this endpoint takes query params only.

    Args:
        start_date (datetime.datetime): start of reporting window (RFC3339)
        end_date (datetime.datetime): end of reporting window (RFC3339)
        granularity (UsageGetMetricsGranularity | Unset): bucket resolution Default:
            UsageGetMetricsGranularity.DAILY.
        timezone (str | Unset): IANA timezone for bucketing periods (e.g., America/Los_Angeles)
            Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsageUsageMetricsResponse | V2ErrorModel
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
        granularity=granularity,
        timezone=timezone,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    granularity: UsageGetMetricsGranularity | Unset = UsageGetMetricsGranularity.DAILY,
    timezone: str | Unset = "UTC",
) -> Response[UsageUsageMetricsResponse | V2ErrorModel]:
    """Get usage metrics (simple)

     Returns infrastructure cost and compute-minute summaries for the caller's user over a date range,
    plus per-bucket chart data. Granularity is hourly (≤24h window) or daily. Use POST /usage/metrics if
    you need richer body params; this endpoint takes query params only.

    Args:
        start_date (datetime.datetime): start of reporting window (RFC3339)
        end_date (datetime.datetime): end of reporting window (RFC3339)
        granularity (UsageGetMetricsGranularity | Unset): bucket resolution Default:
            UsageGetMetricsGranularity.DAILY.
        timezone (str | Unset): IANA timezone for bucketing periods (e.g., America/Los_Angeles)
            Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsageUsageMetricsResponse | V2ErrorModel]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        granularity=granularity,
        timezone=timezone,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    granularity: UsageGetMetricsGranularity | Unset = UsageGetMetricsGranularity.DAILY,
    timezone: str | Unset = "UTC",
) -> UsageUsageMetricsResponse | V2ErrorModel | None:
    """Get usage metrics (simple)

     Returns infrastructure cost and compute-minute summaries for the caller's user over a date range,
    plus per-bucket chart data. Granularity is hourly (≤24h window) or daily. Use POST /usage/metrics if
    you need richer body params; this endpoint takes query params only.

    Args:
        start_date (datetime.datetime): start of reporting window (RFC3339)
        end_date (datetime.datetime): end of reporting window (RFC3339)
        granularity (UsageGetMetricsGranularity | Unset): bucket resolution Default:
            UsageGetMetricsGranularity.DAILY.
        timezone (str | Unset): IANA timezone for bucketing periods (e.g., America/Los_Angeles)
            Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsageUsageMetricsResponse | V2ErrorModel
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity,
            timezone=timezone,
        )
    ).parsed
