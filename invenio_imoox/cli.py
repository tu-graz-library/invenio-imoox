# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for `invenio-imoox` module."""

# import time

import click
from flask import current_app
from flask.cli import with_appcontext
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts

from .services import build_service


@click.group()
def imoox():
    """CLI-group for `invenio-imoox` commands."""


@imoox.command("import")
@with_appcontext
@click.option("--endpoint", required=True)
@click.option("--user-email", type=click.STRING)
@build_service
def import_from_imoox(imoox_service, user_email):
    """Import metadata from endpoint into the repository."""

    user = current_accounts.datastore.get_user_by_email(user_email)
    identity = get_identity(user)

    import_func = current_app.config.get("IMOOX_REPOSITORY_IMPORT_FUNC")
    records = imoox_service.get_records()

    for imoox_record in records:
        try:
            import_func(imoox_record, identity)
        except RuntimeError as error:
            click.secho(str(error), fg="red")
