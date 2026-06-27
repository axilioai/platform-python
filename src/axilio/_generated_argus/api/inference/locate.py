from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.locate_request import LocateRequest
from ...models.locate_response import LocateResponse
from ...types import Response


def _get_kwargs(
    *,
    body: LocateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/inference/locate",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | LocateResponse | None:
    if response.status_code == 200:
        response_200 = LocateResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | LocateResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LocateRequest,
) -> Response[HTTPValidationError | LocateResponse]:
    """Run Locate

    Args:
        body (LocateRequest): Argus /inference/locate request.

            The caller pre-computes OCR via /inference/infer (or reuses cached
            results keyed by frame hash) and passes the text list here. Argus does
            NOT re-run OCR; the VLM call uses the provided `texts` as grounding
            context.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LocateResponse]
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
    body: LocateRequest,
) -> HTTPValidationError | LocateResponse | None:
    """Run Locate

    Args:
        body (LocateRequest): Argus /inference/locate request.

            The caller pre-computes OCR via /inference/infer (or reuses cached
            results keyed by frame hash) and passes the text list here. Argus does
            NOT re-run OCR; the VLM call uses the provided `texts` as grounding
            context.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LocateResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LocateRequest,
) -> Response[HTTPValidationError | LocateResponse]:
    """Run Locate

    Args:
        body (LocateRequest): Argus /inference/locate request.

            The caller pre-computes OCR via /inference/infer (or reuses cached
            results keyed by frame hash) and passes the text list here. Argus does
            NOT re-run OCR; the VLM call uses the provided `texts` as grounding
            context.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LocateResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: LocateRequest,
) -> HTTPValidationError | LocateResponse | None:
    """Run Locate

    Args:
        body (LocateRequest): Argus /inference/locate request.

            The caller pre-computes OCR via /inference/infer (or reuses cached
            results keyed by frame hash) and passes the text list here. Argus does
            NOT re-run OCR; the VLM call uses the provided `texts` as grounding
            context.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LocateResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
