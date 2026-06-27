from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_run_config_variables_type_0_item import RunRunConfigVariablesType0Item


T = TypeVar("T", bound="RunRunConfig")


@_attrs_define
class RunRunConfig:
    """
    Attributes:
        variables (list[RunRunConfigVariablesType0Item] | None):
        phone_id (str | Unset):
    """

    variables: list[RunRunConfigVariablesType0Item] | None
    phone_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        variables: list[dict[str, Any]] | None
        if isinstance(self.variables, list):
            variables = []
            for variables_type_0_item_data in self.variables:
                variables_type_0_item = variables_type_0_item_data.to_dict()
                variables.append(variables_type_0_item)

        else:
            variables = self.variables

        phone_id = self.phone_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "variables": variables,
            }
        )
        if phone_id is not UNSET:
            field_dict["phoneId"] = phone_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_run_config_variables_type_0_item import RunRunConfigVariablesType0Item

        d = dict(src_dict)

        def _parse_variables(data: object) -> list[RunRunConfigVariablesType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                variables_type_0 = []
                _variables_type_0 = data
                for variables_type_0_item_data in _variables_type_0:
                    variables_type_0_item = RunRunConfigVariablesType0Item.from_dict(variables_type_0_item_data)

                    variables_type_0.append(variables_type_0_item)

                return variables_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RunRunConfigVariablesType0Item] | None, data)

        variables = _parse_variables(d.pop("variables"))

        phone_id = d.pop("phoneId", UNSET)

        run_run_config = cls(
            variables=variables,
            phone_id=phone_id,
        )

        return run_run_config
