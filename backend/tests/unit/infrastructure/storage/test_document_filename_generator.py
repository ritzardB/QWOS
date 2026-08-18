"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

File:
    test_document_filename_generator.py

Description:
    Unit tests for the QWOS document filename generator.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date

import pytest

from qwos.infrastructure.storage.document_filename_generator import (
    QWOSDocumentFilenameGenerator,
)


def make_generator() -> QWOSDocumentFilenameGenerator:
    return QWOSDocumentFilenameGenerator()


def test_generates_full_filename() -> None:
    generator = make_generator()

    result = generator.generate(
        employee_number="QW-00002",
        document_category="residence visa",
        issue_date=date(2026, 8, 16),
        expiry_date=date(2027, 8, 15),
        version=1,
        extension=".PDF",
    )

    assert result == (
        "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
    )


def test_generates_filename_without_expiry_date() -> None:
    generator = make_generator()

    result = generator.generate(
        employee_number="QW-00002",
        document_category="employment contract",
        issue_date=date(2026, 2, 1),
        expiry_date=None,
        version=1,
        extension="pdf",
    )

    assert result == (
        "QW-00002_EMPLOYMENT-CONTRACT_2026-02-01_V01.pdf"
    )


def test_generates_filename_without_dates() -> None:
    generator = make_generator()

    result = generator.generate(
        employee_number="QW-00002",
        document_category="other",
        issue_date=None,
        expiry_date=None,
        version=2,
        extension="jpg",
    )

    assert result == "QW-00002_OTHER_V02.jpg"


def test_normalizes_special_characters() -> None:
    generator = make_generator()

    result = generator.generate(
        employee_number="qw 00002",
        document_category="work_permit!",
        issue_date=date(2026, 8, 16),
        expiry_date=date(2027, 8, 15),
        version=3,
        extension=".Pdf",
    )

    assert result == (
        "QW-00002_WORK-PERMIT_2026-08-16_2027-08-15_V03.pdf"
    )


def test_rejects_zero_version() -> None:
    generator = make_generator()

    with pytest.raises(ValueError, match="version"):
        generator.generate(
            employee_number="QW-00002",
            document_category="passport",
            issue_date=None,
            expiry_date=None,
            version=0,
            extension="pdf",
        )


def test_rejects_empty_extension() -> None:
    generator = make_generator()

    with pytest.raises(
        ValueError,
        match="extension is required",
    ):
        generator.generate(
            employee_number="QW-00002",
            document_category="passport",
            issue_date=None,
            expiry_date=None,
            version=1,
            extension="",
        )