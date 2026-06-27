from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_revision_summary import WorkflowRevisionSummary


T = TypeVar("T", bound="WorkflowListRevisionsResponse")


@_attrs_define
class WorkflowListRevisionsResponse:
    """
    Attributes:
        revisions (list[WorkflowRevisionSummary] | None):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    revisions: list[WorkflowRevisionSummary] | None
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        revisions: list[dict[str, Any]] | None
        if isinstance(self.revisions, list):
            revisions = []
            for revisions_type_0_item_data in self.revisions:
                revisions_type_0_item = revisions_type_0_item_data.to_dict()
                revisions.append(revisions_type_0_item)

        else:
            revisions = self.revisions

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "revisions": revisions,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workflow_revision_summary import WorkflowRevisionSummary

        d = dict(src_dict)

        def _parse_revisions(data: object) -> list[WorkflowRevisionSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                revisions_type_0 = []
                _revisions_type_0 = data
                for revisions_type_0_item_data in _revisions_type_0:
                    revisions_type_0_item = WorkflowRevisionSummary.from_dict(revisions_type_0_item_data)

                    revisions_type_0.append(revisions_type_0_item)

                return revisions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkflowRevisionSummary] | None, data)

        revisions = _parse_revisions(d.pop("revisions"))

        schema = d.pop("$schema", UNSET)

        workflow_list_revisions_response = cls(
            revisions=revisions,
            schema=schema,
        )

        return workflow_list_revisions_response
