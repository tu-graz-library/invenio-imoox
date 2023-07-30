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
from invenio_records_lom.utils import LOMMetadata
from invenio_records_resources.services.records.results import RecordItem
from requests import get


def get_records_from_imoox(endpoint: str) -> dict:
    """Get the response from imoox."""
    response = get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()


def create_then_publish(
    lom_metadata: LOMMetadata,
    identity: Identity,
) -> RecordItem:
    """Create and publish function."""
    service = current_records_lom.records_service

    draft = service.create(data=lom_metadata.json, identity=identity)

    # to prevent the race condition bug.
    # see https://github.com/inveniosoftware/invenio-rdm-records/issues/809
    sleep(0.5)

    return service.publish(id_=draft.id, identity=identity)
