from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.usage_chart_data_point import UsageChartDataPoint


T = TypeVar("T", bound="UsageInfrastructureCosts")


@_attrs_define
class UsageInfrastructureCosts:
    """
    Attributes:
        change (float):
        chart_data (list[UsageChartDataPoint] | None):
        this_period (float):
        total (float):
    """

    change: float
    chart_data: list[UsageChartDataPoint] | None
    this_period: float
    total: float

    def to_dict(self) -> dict[str, Any]:
        change = self.change

        chart_data: list[dict[str, Any]] | None
        if isinstance(self.chart_data, list):
            chart_data = []
            for chart_data_type_0_item_data in self.chart_data:
                chart_data_type_0_item = chart_data_type_0_item_data.to_dict()
                chart_data.append(chart_data_type_0_item)

        else:
            chart_data = self.chart_data

        this_period = self.this_period

        total = self.total

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "change": change,
                "chart_data": chart_data,
                "this_period": this_period,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_chart_data_point import UsageChartDataPoint

        d = dict(src_dict)
        change = d.pop("change")

        def _parse_chart_data(data: object) -> list[UsageChartDataPoint] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                chart_data_type_0 = []
                _chart_data_type_0 = data
                for chart_data_type_0_item_data in _chart_data_type_0:
                    chart_data_type_0_item = UsageChartDataPoint.from_dict(chart_data_type_0_item_data)

                    chart_data_type_0.append(chart_data_type_0_item)

                return chart_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageChartDataPoint] | None, data)

        chart_data = _parse_chart_data(d.pop("chart_data"))

        this_period = d.pop("this_period")

        total = d.pop("total")

        usage_infrastructure_costs = cls(
            change=change,
            chart_data=chart_data,
            this_period=this_period,
            total=total,
        )

        return usage_infrastructure_costs
