from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_chart_data_point import UsageChartDataPoint
    from ..models.usage_compute_minutes import UsageComputeMinutes
    from ..models.usage_cost_by_product import UsageCostByProduct
    from ..models.usage_infrastructure_costs import UsageInfrastructureCosts


T = TypeVar("T", bound="UsageUsageMetricsResponse")


@_attrs_define
class UsageUsageMetricsResponse:
    """
    Attributes:
        compute_minutes (UsageComputeMinutes):
        cost_by_product (UsageCostByProduct):
        granularity (str):
        inference_chart_data (list[UsageChartDataPoint] | None):
        infra_costs (UsageInfrastructureCosts):
        period_end (datetime.datetime):
        period_start (datetime.datetime):
        session_chart_data (list[UsageChartDataPoint] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    compute_minutes: UsageComputeMinutes
    cost_by_product: UsageCostByProduct
    granularity: str
    inference_chart_data: list[UsageChartDataPoint] | None
    infra_costs: UsageInfrastructureCosts
    period_end: datetime.datetime
    period_start: datetime.datetime
    session_chart_data: list[UsageChartDataPoint] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        compute_minutes = self.compute_minutes.to_dict()

        cost_by_product = self.cost_by_product.to_dict()

        granularity = self.granularity

        inference_chart_data: list[dict[str, Any]] | None
        if isinstance(self.inference_chart_data, list):
            inference_chart_data = []
            for inference_chart_data_type_0_item_data in self.inference_chart_data:
                inference_chart_data_type_0_item = inference_chart_data_type_0_item_data.to_dict()
                inference_chart_data.append(inference_chart_data_type_0_item)

        else:
            inference_chart_data = self.inference_chart_data

        infra_costs = self.infra_costs.to_dict()

        period_end = self.period_end.isoformat()

        period_start = self.period_start.isoformat()

        session_chart_data: list[dict[str, Any]] | None
        if isinstance(self.session_chart_data, list):
            session_chart_data = []
            for session_chart_data_type_0_item_data in self.session_chart_data:
                session_chart_data_type_0_item = session_chart_data_type_0_item_data.to_dict()
                session_chart_data.append(session_chart_data_type_0_item)

        else:
            session_chart_data = self.session_chart_data

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "compute_minutes": compute_minutes,
                "cost_by_product": cost_by_product,
                "granularity": granularity,
                "inference_chart_data": inference_chart_data,
                "infra_costs": infra_costs,
                "period_end": period_end,
                "period_start": period_start,
                "session_chart_data": session_chart_data,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_chart_data_point import UsageChartDataPoint
        from ..models.usage_compute_minutes import UsageComputeMinutes
        from ..models.usage_cost_by_product import UsageCostByProduct
        from ..models.usage_infrastructure_costs import UsageInfrastructureCosts

        d = dict(src_dict)
        compute_minutes = UsageComputeMinutes.from_dict(d.pop("compute_minutes"))

        cost_by_product = UsageCostByProduct.from_dict(d.pop("cost_by_product"))

        granularity = d.pop("granularity")

        def _parse_inference_chart_data(data: object) -> list[UsageChartDataPoint] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                inference_chart_data_type_0 = []
                _inference_chart_data_type_0 = data
                for inference_chart_data_type_0_item_data in _inference_chart_data_type_0:
                    inference_chart_data_type_0_item = UsageChartDataPoint.from_dict(
                        inference_chart_data_type_0_item_data
                    )

                    inference_chart_data_type_0.append(inference_chart_data_type_0_item)

                return inference_chart_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageChartDataPoint] | None, data)

        inference_chart_data = _parse_inference_chart_data(d.pop("inference_chart_data"))

        infra_costs = UsageInfrastructureCosts.from_dict(d.pop("infra_costs"))

        period_end = datetime.datetime.fromisoformat(d.pop("period_end"))

        period_start = datetime.datetime.fromisoformat(d.pop("period_start"))

        def _parse_session_chart_data(data: object) -> list[UsageChartDataPoint] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                session_chart_data_type_0 = []
                _session_chart_data_type_0 = data
                for session_chart_data_type_0_item_data in _session_chart_data_type_0:
                    session_chart_data_type_0_item = UsageChartDataPoint.from_dict(session_chart_data_type_0_item_data)

                    session_chart_data_type_0.append(session_chart_data_type_0_item)

                return session_chart_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageChartDataPoint] | None, data)

        session_chart_data = _parse_session_chart_data(d.pop("session_chart_data"))

        schema = d.pop("$schema", UNSET)

        usage_usage_metrics_response = cls(
            compute_minutes=compute_minutes,
            cost_by_product=cost_by_product,
            granularity=granularity,
            inference_chart_data=inference_chart_data,
            infra_costs=infra_costs,
            period_end=period_end,
            period_start=period_start,
            session_chart_data=session_chart_data,
            schema=schema,
        )

        return usage_usage_metrics_response
