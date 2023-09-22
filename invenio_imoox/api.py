# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""API functions."""
from flask_principal import Identity
from invenio_records_lom.utils import LOMMetadata
from invenio_records_resources.services.records.results import RecordItem

from .converter import convert
from .utils import create_then_publish


def import_record(imoox_record: dict, identity: Identity) -> RecordItem:
    """Import record."""
    pids = {
        "imoox": {
            "provider": "imoox",
            "identifier": f"{imoox_record['id']}-imoox",
        },
    }
    lom_metadata = LOMMetadata.create(
        resource_type="link",
        pids=pids,
        overwritable=True,
    )

    convert(imoox_record, lom_metadata)
    return create_then_publish(lom_metadata, identity)
