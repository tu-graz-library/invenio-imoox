# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Utils for invenio-imoox."""
from __future__ import annotations

from time import sleep

from flask_principal import Identity
from invenio_records_lom import current_records_lom
from invenio_records_lom.utils import LOMMetadata
from invenio_records_resources.services.records.results import RecordItem
from invenio_search import RecordsSearch
from invenio_search.engine import dsl
from requests import get


def get_records_from_imoox(endpoint: str) -> dict:
    """Get the response from imoox."""
    response = get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()


def check_about_duplicate(value: str) -> str | None:
    """Check if the record with the ac number is already within the database."""
    search = RecordsSearch(index="lomrecords-records-record-v1.0.0")
    search.query = dsl.Q(
        "bool",
        must=[
            dsl.Q(
                "match",
                **{
                    "metadata.general.identifier.catalog": "imoox",
                },
            ),
            dsl.Q(
                "match",
                **{
                    "metadata.general.identifier.entry.langstring.#text": value,
                },
            ),
        ],
    )
    results = search.execute()

    if len(results) > 0:
        return results[0]["id"]
    return None


def create_then_publish(
    lom_metadata: LOMMetadata,
    identity: Identity,
) -> RecordItem:
    """Create and publish function."""
    service = current_records_lom.records_service
    imoox_id = lom_metadata.get_identifier("imoox")

    if pid := check_about_duplicate(imoox_id):
        msg = f"Imoox id: {imoox_id} is duplicate record with pid: {pid}"
        raise RuntimeError(msg)

    draft = service.create(data=lom_metadata.json, identity=identity)

    # to prevent the race condition bug.
    # see https://github.com/inveniosoftware/invenio-rdm-records/issues/809
    sleep(0.5)

    return service.publish(id_=draft.id, identity=identity)
