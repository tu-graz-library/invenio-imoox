# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Technische Universität Graz
#
# invenio-imoox is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Converter Module to facilitate conversion of metadata."""


from html import unescape
from typing import Any

from invenio_records_lom.utils import LOMMetadata


class Converter:
    """Converter base class."""

    def convert(self, parent: dict, record: LOMMetadata) -> None:
        """Convert method."""
        for attribute, value in parent.items():
            self.process(attribute, value, record)

    def process(
        self,
        attribute: str,
        value: Any,  # noqa: ANN401
        record: LOMMetadata,
    ) -> None:
        """Execute the corresponding method to the attribute."""

        def func_not_found(*_: dict, **__: dict) -> None:
            msg = f"NO convert method for {attribute}"
            raise ValueError(msg)

        convert_func = getattr(self, f"convert_{attribute}", func_not_found)
        return convert_func(value, record)


class MoocToLOM(Converter):
    """Convert class to convert Mooc to LOM."""

    def __init__(self) -> None:
        """Construct MoocToLOM."""
        self.language = ""

    def set_language(self, parent: dict) -> None:
        """Set default language for langstring."""
        if "languages" not in parent["attributes"]:
            return

        if len(parent["attributes"]["languages"]) == 0:
            return

        self.language = parent["attributes"]["languages"][0]

    def convert(self, parent: dict, record: LOMMetadata) -> dict:
        """Convert overrides base convert method to return the record."""
        self.set_language(parent)

        super().convert(parent, record)

    def convert_id(self, value: str, record: LOMMetadata) -> None:
        """Convert id attribute."""
        record.append_identifier(value, catalog="imoox")

    def convert_type(self, value: str, record: LOMMetadata) -> None:
        """Convert type attribute."""

    def convert_attributes(self, value: str, record: LOMMetadata) -> None:
        """Convert attributes attribute."""
        super().convert(value, record)

    def convert_name(self, value: str, record: LOMMetadata) -> None:
        """Convert name attribute."""
        record.set_title(value, language_code=self.language)

    def convert_courseCode(self, value: str, record: LOMMetadata) -> None:
        """Convert courseCode attribute."""

    def convert_courseMode(self, value: str, record: LOMMetadata) -> None:
        """Convert courseMode attribute."""

    def convert_abstract(self, value: str, record: LOMMetadata) -> None:
        """Convert abstract attribute."""
        record.append_description(unescape(value), language_code=self.language)

    def convert_description(self, value: str, record: LOMMetadata) -> None:
        """Convert description attribute."""
        record.append_description(unescape(value), language_code=self.language)

    def convert_languages(self, value: str, record: LOMMetadata) -> None:
        """Convert languages attribute."""
        record.append_language(value)

    def convert_startDate(self, value: str, record: LOMMetadata) -> None:
        """Convert startDate attribute."""
        record.set_datetime(value.split("T")[0])

    def convert_availableUntil(self, value: str, record: LOMMetadata) -> None:
        """Convert availableUntil attribute."""

    def convert_endDate(self, value: str, record: LOMMetadata) -> None:
        """Convert endDate attribute."""

    def convert_image(self, value: str, record: LOMMetadata) -> None:
        """Convert image attribute."""
        record.set_thumbnail(value)

    def convert_video(self, value: str, record: LOMMetadata) -> None:
        """Convert video attribute."""

    def convert_instructors(self, value: list, record: LOMMetadata) -> None:
        """Convert instructors attribute."""
        for instructor in value:
            description = instructor.get("description", None)

            record.append_contribute(
                instructor["name"],
                role="Author",
                description=description,
            )

    def convert_learningobjectives(self, value: list, record: LOMMetadata) -> None:
        """Convert learningobjectives attribute."""
        for desc in value:
            record.append_educational_description(desc, self.language)

    def convert_duration(self, value: str, record: LOMMetadata) -> None:
        """Convert duration attribute."""
        record.set_duration(value, self.language)

    def convert_partnerInstitute(self, value: list, record: LOMMetadata) -> None:
        """Convert partnerInstitute attribute."""
        for partner in value:
            record.append_contribute(partner["name"], role="Publisher")

    def convert_moocProvider(self, value: dict, record: LOMMetadata) -> None:
        """Convert moocProvider attribute.

        value = {"name": "", "url": "", "logo": ""}
        """
        record.append_metametadata_contribute(
            name=value["name"],
            url=value["url"],
            logo=value["logo"],
            role="Provider",
        )

    def convert_url(self, value: str, record: LOMMetadata) -> None:
        """Convert url attribute."""
        record.set_location(value)

    def convert_workload(self, value: str, record: LOMMetadata) -> None:
        """Convert workload attribute."""
        record.set_typical_learning_time(value, "workload")

    def convert_courseLicenses(self, value: list, record: LOMMetadata) -> None:
        """Convert courseLicenses attribute."""
        record.set_rights_url(value[0]["url"])

    def convert_access(self, value: str, record: LOMMetadata) -> None:
        """Convert access attribute."""

    def convert_categories(self, value: str, record: LOMMetadata) -> None:
        """Convert categories attribute."""
        super().convert(value, record)

    def convert_oefos(self, value: list, record: LOMMetadata) -> None:
        """Convert oefos attribute."""
        for taxon_id in value:
            record.append_oefos_id(taxon_id)


def convert(imoox_record: dict, lom_metadata: LOMMetadata) -> None:
    """Convert the imoox representation to lom."""
    visitor = MoocToLOM()
    visitor.convert(imoox_record, lom_metadata)
