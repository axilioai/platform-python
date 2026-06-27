from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.text_element_input import TextElementInput


T = TypeVar("T", bound="LocateRequest")


@_attrs_define
class LocateRequest:
    """Argus /inference/locate request.

    The caller pre-computes OCR via /inference/infer (or reuses cached
    results keyed by frame hash) and passes the text list here. Argus does
    NOT re-run OCR; the VLM call uses the provided `texts` as grounding
    context.

        Attributes:
            image (str): Base64 encoded image (PNG or JPEG)
            query (str): Natural-language target description
            model (None | str | Unset): VLM model to use; must be one of the models from GET /inference/models. Omit to use
                the server's configured default. The system prompt is fixed to the element-locator task.
            texts (list[TextElementInput] | Unset): Pre-computed OCR text elements. Empty list means Argus skips OCR
                grounding and asks the VLM to locate from the image alone.
    """

    image: str
    query: str
    model: None | str | Unset = UNSET
    texts: list[TextElementInput] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        query = self.query

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        texts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.texts, Unset):
            texts = []
            for texts_item_data in self.texts:
                texts_item = texts_item_data.to_dict()
                texts.append(texts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "query": query,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model
        if texts is not UNSET:
            field_dict["texts"] = texts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.text_element_input import TextElementInput

        d = dict(src_dict)
        image = d.pop("image")

        query = d.pop("query")

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        _texts = d.pop("texts", UNSET)
        texts: list[TextElementInput] | Unset = UNSET
        if _texts is not UNSET:
            texts = []
            for texts_item_data in _texts:
                texts_item = TextElementInput.from_dict(texts_item_data)

                texts.append(texts_item)

        locate_request = cls(
            image=image,
            query=query,
            model=model,
            texts=texts,
        )

        locate_request.additional_properties = d
        return locate_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
