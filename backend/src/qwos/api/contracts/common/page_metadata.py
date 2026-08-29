"""
===============================================================================
Quantum Workforce OS (QWOS)

Core Contracts

File:
    page_metadata.py
===============================================================================
"""

from __future__ import annotations

from qwos.api.contracts.responses.common.base_response import BaseResponse


class PageMetadata(BaseResponse):
    page: int

    page_size: int

    total_records: int

    total_pages: int

    has_previous: bool

    has_next: bool
