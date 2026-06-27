from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_run_config import RunRunConfig
    from ..models.run_run_time_config import RunRunTimeConfig


T = TypeVar("T", bound="RunRunCreateRequest")


@_attrs_define
class RunRunCreateRequest:
    """
    Attributes:
        number_of_runs (int):
        run_time (RunRunTimeConfig):
        runs (list[RunRunConfig] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    number_of_runs: int
    run_time: RunRunTimeConfig
    runs: list[RunRunConfig] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        number_of_runs = self.number_of_runs

        run_time = self.run_time.to_dict()

        runs: list[dict[str, Any]] | None
        if isinstance(self.runs, list):
            runs = []
            for runs_type_0_item_data in self.runs:
                runs_type_0_item = runs_type_0_item_data.to_dict()
                runs.append(runs_type_0_item)

        else:
            runs = self.runs

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "numberOfRuns": number_of_runs,
                "runTime": run_time,
                "runs": runs,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_run_config import RunRunConfig
        from ..models.run_run_time_config import RunRunTimeConfig

        d = dict(src_dict)
        number_of_runs = d.pop("numberOfRuns")

        run_time = RunRunTimeConfig.from_dict(d.pop("runTime"))

        def _parse_runs(data: object) -> list[RunRunConfig] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                runs_type_0 = []
                _runs_type_0 = data
                for runs_type_0_item_data in _runs_type_0:
                    runs_type_0_item = RunRunConfig.from_dict(runs_type_0_item_data)

                    runs_type_0.append(runs_type_0_item)

                return runs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RunRunConfig] | None, data)

        runs = _parse_runs(d.pop("runs"))

        schema = d.pop("$schema", UNSET)

        run_run_create_request = cls(
            number_of_runs=number_of_runs,
            run_time=run_time,
            runs=runs,
            schema=schema,
        )

        return run_run_create_request
