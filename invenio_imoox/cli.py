# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for `invenio-imoox` module."""


from click import STRING, echo, group, option
from flask.cli import with_appcontext
from invenio_config_tugraz import get_identity_from_user_by_email

from .api import import_record
from .utils import get_records_from_imoox


@group()
def imoox() -> None:
    """CLI-group for `invenio-imoox` commands."""


@imoox.command("import")
@with_appcontext
@option("--endpoint", required=True)
@option("--user-email", type=STRING, default="imoox@tugraz.at")
def import_from_imoox(endpoint: str, user_email: str) -> None:
    """Import metadata from endpoint into the repository."""
    identity = get_identity_from_user_by_email(email=user_email)
    imoox_records = get_records_from_imoox(endpoint)

    for imoox_record in imoox_records["data"]:
        try:
            record = import_record(imoox_record, identity)
            echo(record.id)
        except RuntimeError as error:
            echo(error)
