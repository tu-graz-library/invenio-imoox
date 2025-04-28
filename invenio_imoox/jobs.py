# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Jobs."""


from invenio_jobs.jobs import JobType

from .tasks import import_imoox_records


class ImportImooxRecordsJob(JobType):
    """Import iMooX records."""

    id = "import_imoox_records"
    title = "Import iMooX Records"
    description = "Import imoox records."

    task = import_imoox_records
