# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-imoox is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Provides API for iMooX."""

from .ext import InvenioIMooX
from .version import __version__

__all__ = ("__version__", "InvenioIMooX")
