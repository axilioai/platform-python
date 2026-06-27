from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_historic_run import RunHistoricRun


T = TypeVar("T", bound="RunHistoricRunsResponse")


@_attrs_define
class RunHistoricRunsResponse:
    """
    Attributes:
        limit (int):
        offset (int):
        runs (list[RunHistoricRun] | None):
        total (int):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    limit: int
    offset: int
    runs: list[RunHistoricRun] | None
    total: int
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        runs: list[dict[str, Any]] | None
        if isinstance(self.runs, list):
            runs = []
            for runs_type_0_item_data in self.runs:
                runs_type_0_item = runs_type_0_item_data.to_dict()
                runs.append(runs_type_0_item)

        else:
            runs = self.runs

        total = self.total

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
                "runs": runs,
                "total": total,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_historic_run import RunHistoricRun

        d = dict(src_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        def _parse_runs(data: object) -> list[RunHistoricRun] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                runs_type_0 = []
                _runs_type_0 = data
                for runs_type_0_item_data in _runs_type_0:
                    runs_type_0_item = RunHistoricRun.from_dict(runs_type_0_item_data)

                    runs_type_0.append(runs_type_0_item)

                return runs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RunHistoricRun] | None, data)

        runs = _parse_runs(d.pop("runs"))

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        run_historic_runs_response = cls(
            limit=limit,
            offset=offset,
            runs=runs,
            total=total,
            schema=schema,
        )

        return run_historic_runs_response
