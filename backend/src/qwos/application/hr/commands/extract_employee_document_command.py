"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

HR Module

File:
    extract_employee_document_command.py

Description:
    Command used to request extraction of structured data from an employee
    document.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from qwos.application.common.context.request_context import RequestContext


@dataclass(frozen=True, slots=True)
class ExtractEmployeeDocumentCommand:
    """
    Request extraction of structured data from an employee document.
    """

    employee_id: str
    document_id: str
    request_context: RequestContext