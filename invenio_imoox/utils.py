# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Utils for invenio-imoox."""

from time import sleep

from flask_principal import Identity
from invenio_records_lom import current_records_lom
from invenio_records_resources.services.records.results import RecordItem
from requests import get

from .converter import MoocToLOM


def get_records_from_imoox(endpoint: str) -> dict:
    """Get the response from imoox."""
    response = get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()


def convert(imoox_records: list) -> list:
    """Convert the imoox representation to lom."""
    converter = MoocToLOM()
    lom_records = []

    for imoox_record in imoox_records["data"]:
        lom_records.append(converter.convert(imoox_record))

    return lom_records


def create_then_publish(lom_record: dict, identity: Identity) -> RecordItem:
    """Create and publish function."""
    service = current_records_lom.records_service

    data = {
        "access": {"record": "public", "files": "public"},
        "files": {"enabled": False},
        "metadata": lom_record,
        "resource_type": "link",
    }

    draft = service.create(data=data, identity=identity)

    # to prevent the race condition bug.
    # see https://github.com/inveniosoftware/invenio-rdm-records/issues/809
    sleep(0.5)

    return service.publish(id_=draft.id, identity=identity)
