# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Provides API for iMooX."""

from .ext import InvenioIMooX

__version__ = "0.4.1"

__all__ = (
    "InvenioIMooX",
    "__version__",
)
