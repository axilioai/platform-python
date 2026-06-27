from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.phone_phone_app_summary_app_metadata import PhonePhoneAppSummaryAppMetadata


T = TypeVar("T", bound="PhonePhoneAppSummary")


@_attrs_define
class PhonePhoneAppSummary:
    """
    Attributes:
        android_package_name (str):
        app_metadata (PhonePhoneAppSummaryAppMetadata):
        category (str):
        create_date (datetime.datetime):
        description (None | str):
        icon_url (None | str):
        id (str):
        ios_app_store_id (None | str):
        is_supported (bool):
        model_datasets (list[str] | None):
        model_status (str):
        model_trained_at (datetime.datetime | None):
        name (str):
        platform (str):
        slug (str):
        update_date (datetime.datetime):
        version (None | str):
    """

    android_package_name: str
    app_metadata: PhonePhoneAppSummaryAppMetadata
    category: str
    create_date: datetime.datetime
    description: None | str
    icon_url: None | str
    id: str
    ios_app_store_id: None | str
    is_supported: bool
    model_datasets: list[str] | None
    model_status: str
    model_trained_at: datetime.datetime | None
    name: str
    platform: str
    slug: str
    update_date: datetime.datetime
    version: None | str

    def to_dict(self) -> dict[str, Any]:
        android_package_name = self.android_package_name

        app_metadata = self.app_metadata.to_dict()

        category = self.category

        create_date = self.create_date.isoformat()

        description: None | str
        description = self.description

        icon_url: None | str
        icon_url = self.icon_url

        id = self.id

        ios_app_store_id: None | str
        ios_app_store_id = self.ios_app_store_id

        is_supported = self.is_supported

        model_datasets: list[str] | None
        if isinstance(self.model_datasets, list):
            model_datasets = self.model_datasets

        else:
            model_datasets = self.model_datasets

        model_status = self.model_status

        model_trained_at: None | str
        if isinstance(self.model_trained_at, datetime.datetime):
            model_trained_at = self.model_trained_at.isoformat()
        else:
            model_trained_at = self.model_trained_at

        name = self.name

        platform = self.platform

        slug = self.slug

        update_date = self.update_date.isoformat()

        version: None | str
        version = self.version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "android_package_name": android_package_name,
                "app_metadata": app_metadata,
                "category": category,
                "create_date": create_date,
                "description": description,
                "icon_url": icon_url,
                "id": id,
                "ios_app_store_id": ios_app_store_id,
                "is_supported": is_supported,
                "model_datasets": model_datasets,
                "model_status": model_status,
                "model_trained_at": model_trained_at,
                "name": name,
                "platform": platform,
                "slug": slug,
                "update_date": update_date,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_phone_app_summary_app_metadata import PhonePhoneAppSummaryAppMetadata

        d = dict(src_dict)
        android_package_name = d.pop("android_package_name")

        app_metadata = PhonePhoneAppSummaryAppMetadata.from_dict(d.pop("app_metadata"))

        category = d.pop("category")

        create_date = datetime.datetime.fromisoformat(d.pop("create_date"))

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        def _parse_icon_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        icon_url = _parse_icon_url(d.pop("icon_url"))

        id = d.pop("id")

        def _parse_ios_app_store_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        ios_app_store_id = _parse_ios_app_store_id(d.pop("ios_app_store_id"))

        is_supported = d.pop("is_supported")

        def _parse_model_datasets(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                model_datasets_type_0 = cast(list[str], data)

                return model_datasets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        model_datasets = _parse_model_datasets(d.pop("model_datasets"))

        model_status = d.pop("model_status")

        def _parse_model_trained_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_trained_at_type_0 = datetime.datetime.fromisoformat(data)

                return model_trained_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        model_trained_at = _parse_model_trained_at(d.pop("model_trained_at"))

        name = d.pop("name")

        platform = d.pop("platform")

        slug = d.pop("slug")

        update_date = datetime.datetime.fromisoformat(d.pop("update_date"))

        def _parse_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        version = _parse_version(d.pop("version"))

        phone_phone_app_summary = cls(
            android_package_name=android_package_name,
            app_metadata=app_metadata,
            category=category,
            create_date=create_date,
            description=description,
            icon_url=icon_url,
            id=id,
            ios_app_store_id=ios_app_store_id,
            is_supported=is_supported,
            model_datasets=model_datasets,
            model_status=model_status,
            model_trained_at=model_trained_at,
            name=name,
            platform=platform,
            slug=slug,
            update_date=update_date,
            version=version,
        )

        return phone_phone_app_summary
