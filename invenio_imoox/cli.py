# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for `invenio-imoox` module."""

import json

import click
import requests

from .converter import MoocToLOM


def get_records_from_imoox(endpoint: str) -> dict:
    """Get the response from imoox."""
    response = requests.get(endpoint)
    return json.loads(response.text.encode("utf-8"))


def convert(imoox_records: list) -> dict:
    """Convert the imoox representation to lom."""
    converter = MoocToLOM()
    lom_records = []

    for imoox_record in imoox_records["data"]:
        lom_records.append(converter.convert(imoox_record))

    return lom_records


@click.group()
def imoox():
    """CLI-group for `invenio-imoox` commands."""
    pass


@imoox.command("import")
@click.option("--endpoint", required=True)
def import_from_imoox(endpoint):
    """Import metadata from endpoint into the repository."""
    imoox_records = get_records_from_imoox(endpoint)
    lom_records = convert(imoox_records)
    return lom_records
