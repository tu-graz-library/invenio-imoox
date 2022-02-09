# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Technische Universität Graz
#
# invenio-imoox is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Converter Module to facilitate conversion of metadata."""

from functools import wraps


def ensure_value_str_not_empty(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args[1]) == 0:
            return
        return func(*args, **kwargs)

    return wrapper


def ensure_value_str(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not isinstance(args[1], str):
            return
        return func(*args, **kwargs)

    return wrapper


def ensure_value_list(list_type=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def ensure_attribute_list(query):
    prop, base, sub = query.split(".")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            obj = getattr(args[0], prop)
            if base not in obj:
                obj[base] = {}
            if sub not in obj[base]:
                obj[base][sub] = []

            return func(*args, **kwargs)

        return wrapper

    return decorator


class Converter:
    """Converter base class."""

    def convert(self, parent):
        """Base convert method."""
        for attribute, value in parent.items():
            self.process(attribute, value)

    def process(self, attribute: str, value):
        """Execute the corresponding method to the attribute."""

        def func_not_found(*args, **kwargs):
            raise ValueError(f"NO convert method for {attribute}")

        convert_func = getattr(self, f"convert_{attribute}", func_not_found)
        return convert_func(value)


class MoocToLOM(Converter):
    """Convert class to convert Mooc to LOM"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.record = {
            "general": {},
            "custom": {},
            "metametadata": {},
            "technical": {},
            "rights": {},
            "educational": {},
        }

    def convert(self, parent):
        """Convert overrides base convert method to return the record."""
        self.reset()

        super().convert(parent)
        return self.record

    def convert_id(self, value):
        """Convert id attribute."""
        pass

    def convert_type(self, value):
        """Convert type attribute."""
        pass

    def convert_attributes(self, value):
        """Convert attributes attribute."""
        self.convert(value)

    @ensure_value_str
    def convert_name(self, value):
        """Convert name attribute."""
        self.record["general"]["title"] = value

    def convert_courseCode(self, value):
        """Convert courseCode attribute."""
        pass

    def convert_courseMode(self, value):
        """Convert courseMode attribute."""
        pass

    @ensure_value_str
    @ensure_value_str_not_empty
    @ensure_attribute_list("record.general.description")
    def convert_abstract(self, value):
        """Convert abstract attribute."""
        self.record["general"]["description"].append(value)

    @ensure_value_str
    @ensure_value_str_not_empty
    @ensure_attribute_list("record.general.description")
    def convert_description(self, value):
        """Convert description attribute."""
        self.record["general"]["description"].append(value)

    @ensure_value_list()
    def convert_languages(self, value):
        """Convert languages attribute."""
        self.record["general"]["language"] = value

    def convert_startDate(self, value):
        """Convert startDate attribute."""
        pass

    def convert_availableUntil(self, value):
        """Convert availableUntil attribute."""
        pass

    def convert_endDate(self, value):
        """Convert endDate attribute."""
        pass

    def convert_image(self, value):
        """Convert image attribute."""
        self.record["custom"]["thumbnail"] = value

    def convert_video(self, value):
        """Convert video attribute."""
        pass

    @ensure_value_list({"name": str, "description": str})
    @ensure_attribute_list("record.metametadata.contribute")
    def convert_instructors(self, value):
        """Convert instructors attribute."""
        for instructor in value:
            self.record["metametadata"]["contribute"].append(
                {
                    "role": {"value": "Instructor"},
                    "entity": instructor["name"],
                    "description": instructor["description"],
                }
            )

    def convert_learningobjectives(self, value):
        """Convert learningobjectives attribute."""
        self.record["educational"]["description"] = value

    def convert_duration(self, value):
        """Convert duration attribute."""
        self.record["technical"]["duration"] = value

    @ensure_value_list({"name": str})
    @ensure_attribute_list("record.metametadata.contribute")
    def convert_partnerInstitute(self, value):
        """Convert partnerInstitute attribute."""
        for partner in value:
            self.record["metametadata"]["contribute"].append(
                {
                    "role": {"value": "partner"},
                    "entity": partner["name"],
                }
            )

    def convert_moocProvider(self, value):
        """Convert moocProvider attribute."""

    def convert_url(self, value):
        """Convert url attribute."""
        self.record["technical"]["location"] = value

    def convert_workload(self, value):
        """Convert workload attribute."""

    def convert_courseLicenses(self, value):
        """Convert courseLicenses attribute."""
        self.record["rights"]["copyrightandotherrestrictions"] = value

    def convert_access(self, value):
        """Convert access attribute."""
        pass
