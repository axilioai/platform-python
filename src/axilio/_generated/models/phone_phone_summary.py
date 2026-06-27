from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phone_phone_summary_phone_metadata import PhonePhoneSummaryPhoneMetadata


T = TypeVar("T", bound="PhonePhoneSummary")


@_attrs_define
class PhonePhoneSummary:
    """
    Attributes:
        agent_version (None | str):
        android_version (None | str):
        create_date (datetime.datetime):
        current_session_id (None | str):
        id (str):
        imei1 (None | str):
        imei2 (None | str):
        last_heartbeat (datetime.datetime | None):
        last_interaction_timestamp (datetime.datetime | None):
        location (None | str):
        model_id (None | str):
        model_name (None | str):
        nickname (None | str):
        one_ui_version (None | str):
        owner_organization_id (None | str):
        ownership_type (str):
        phone_id (str):
        phone_metadata (PhonePhoneSummaryPhoneMetadata):
        phone_name (None | str):
        phone_serial (None | str):
        phone_type (None | str):
        rental_expires_at (datetime.datetime | None):
        status (str):
        update_date (datetime.datetime):
        schema (str | Unset): A URL to the JSON Schema for this object.
    """

    agent_version: None | str
    android_version: None | str
    create_date: datetime.datetime
    current_session_id: None | str
    id: str
    imei1: None | str
    imei2: None | str
    last_heartbeat: datetime.datetime | None
    last_interaction_timestamp: datetime.datetime | None
    location: None | str
    model_id: None | str
    model_name: None | str
    nickname: None | str
    one_ui_version: None | str
    owner_organization_id: None | str
    ownership_type: str
    phone_id: str
    phone_metadata: PhonePhoneSummaryPhoneMetadata
    phone_name: None | str
    phone_serial: None | str
    phone_type: None | str
    rental_expires_at: datetime.datetime | None
    status: str
    update_date: datetime.datetime
    schema: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        agent_version: None | str
        agent_version = self.agent_version

        android_version: None | str
        android_version = self.android_version

        create_date = self.create_date.isoformat()

        current_session_id: None | str
        current_session_id = self.current_session_id

        id = self.id

        imei1: None | str
        imei1 = self.imei1

        imei2: None | str
        imei2 = self.imei2

        last_heartbeat: None | str
        if isinstance(self.last_heartbeat, datetime.datetime):
            last_heartbeat = self.last_heartbeat.isoformat()
        else:
            last_heartbeat = self.last_heartbeat

        last_interaction_timestamp: None | str
        if isinstance(self.last_interaction_timestamp, datetime.datetime):
            last_interaction_timestamp = self.last_interaction_timestamp.isoformat()
        else:
            last_interaction_timestamp = self.last_interaction_timestamp

        location: None | str
        location = self.location

        model_id: None | str
        model_id = self.model_id

        model_name: None | str
        model_name = self.model_name

        nickname: None | str
        nickname = self.nickname

        one_ui_version: None | str
        one_ui_version = self.one_ui_version

        owner_organization_id: None | str
        owner_organization_id = self.owner_organization_id

        ownership_type = self.ownership_type

        phone_id = self.phone_id

        phone_metadata = self.phone_metadata.to_dict()

        phone_name: None | str
        phone_name = self.phone_name

        phone_serial: None | str
        phone_serial = self.phone_serial

        phone_type: None | str
        phone_type = self.phone_type

        rental_expires_at: None | str
        if isinstance(self.rental_expires_at, datetime.datetime):
            rental_expires_at = self.rental_expires_at.isoformat()
        else:
            rental_expires_at = self.rental_expires_at

        status = self.status

        update_date = self.update_date.isoformat()

        schema = self.schema

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_version": agent_version,
                "android_version": android_version,
                "create_date": create_date,
                "current_session_id": current_session_id,
                "id": id,
                "imei1": imei1,
                "imei2": imei2,
                "last_heartbeat": last_heartbeat,
                "last_interaction_timestamp": last_interaction_timestamp,
                "location": location,
                "model_id": model_id,
                "model_name": model_name,
                "nickname": nickname,
                "one_ui_version": one_ui_version,
                "owner_organization_id": owner_organization_id,
                "ownership_type": ownership_type,
                "phone_id": phone_id,
                "phone_metadata": phone_metadata,
                "phone_name": phone_name,
                "phone_serial": phone_serial,
                "phone_type": phone_type,
                "rental_expires_at": rental_expires_at,
                "status": status,
                "update_date": update_date,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phone_phone_summary_phone_metadata import PhonePhoneSummaryPhoneMetadata

        d = dict(src_dict)

        def _parse_agent_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        agent_version = _parse_agent_version(d.pop("agent_version"))

        def _parse_android_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        android_version = _parse_android_version(d.pop("android_version"))

        create_date = datetime.datetime.fromisoformat(d.pop("create_date"))

        def _parse_current_session_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        current_session_id = _parse_current_session_id(d.pop("current_session_id"))

        id = d.pop("id")

        def _parse_imei1(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        imei1 = _parse_imei1(d.pop("imei1"))

        def _parse_imei2(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        imei2 = _parse_imei2(d.pop("imei2"))

        def _parse_last_heartbeat(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_heartbeat_type_0 = datetime.datetime.fromisoformat(data)

                return last_heartbeat_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_heartbeat = _parse_last_heartbeat(d.pop("last_heartbeat"))

        def _parse_last_interaction_timestamp(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_interaction_timestamp_type_0 = datetime.datetime.fromisoformat(data)

                return last_interaction_timestamp_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_interaction_timestamp = _parse_last_interaction_timestamp(d.pop("last_interaction_timestamp"))

        def _parse_location(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        location = _parse_location(d.pop("location"))

        def _parse_model_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        model_id = _parse_model_id(d.pop("model_id"))

        def _parse_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        model_name = _parse_model_name(d.pop("model_name"))

        def _parse_nickname(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        nickname = _parse_nickname(d.pop("nickname"))

        def _parse_one_ui_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        one_ui_version = _parse_one_ui_version(d.pop("one_ui_version"))

        def _parse_owner_organization_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        owner_organization_id = _parse_owner_organization_id(d.pop("owner_organization_id"))

        ownership_type = d.pop("ownership_type")

        phone_id = d.pop("phone_id")

        phone_metadata = PhonePhoneSummaryPhoneMetadata.from_dict(d.pop("phone_metadata"))

        def _parse_phone_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_name = _parse_phone_name(d.pop("phone_name"))

        def _parse_phone_serial(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_serial = _parse_phone_serial(d.pop("phone_serial"))

        def _parse_phone_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_type = _parse_phone_type(d.pop("phone_type"))

        def _parse_rental_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rental_expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return rental_expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        rental_expires_at = _parse_rental_expires_at(d.pop("rental_expires_at"))

        status = d.pop("status")

        update_date = datetime.datetime.fromisoformat(d.pop("update_date"))

        schema = d.pop("$schema", UNSET)

        phone_phone_summary = cls(
            agent_version=agent_version,
            android_version=android_version,
            create_date=create_date,
            current_session_id=current_session_id,
            id=id,
            imei1=imei1,
            imei2=imei2,
            last_heartbeat=last_heartbeat,
            last_interaction_timestamp=last_interaction_timestamp,
            location=location,
            model_id=model_id,
            model_name=model_name,
            nickname=nickname,
            one_ui_version=one_ui_version,
            owner_organization_id=owner_organization_id,
            ownership_type=ownership_type,
            phone_id=phone_id,
            phone_metadata=phone_metadata,
            phone_name=phone_name,
            phone_serial=phone_serial,
            phone_type=phone_type,
            rental_expires_at=rental_expires_at,
            status=status,
            update_date=update_date,
            schema=schema,
        )

        return phone_phone_summary
