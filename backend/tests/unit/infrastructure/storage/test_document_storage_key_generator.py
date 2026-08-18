from __future__ import annotations

import pytest

from qwos.infrastructure.storage.document_storage_key_generator import (
    QWOSDocumentStorageKeyGenerator,
)


def make_generator() -> QWOSDocumentStorageKeyGenerator:
    return QWOSDocumentStorageKeyGenerator()


def test_generates_standard_storage_key() -> None:
    generator = make_generator()

    result = generator.generate(
        employee_number="QW-00002",
        document_category="Residence Visa",
        stored_filename=(
            "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
        ),
    )

    assert result == (
        "employees/QW-00002/documents/residence-visa/"
        "QW-00002_RESIDENCE-VISA_2026-08-16_2027-08-15_V01.pdf"
    )


def test_normalizes_employee_number_and_category() -> None:
    generator = make_generator()

    result = generator.generate(
        employee_number="qw 00002",
        document_category="work permit!",
        stored_filename="QW-00002_WORK-PERMIT_V01.pdf",
    )

    assert result == (
        "employees/QW-00002/documents/work-permit/"
        "QW-00002_WORK-PERMIT_V01.pdf"
    )


def test_rejects_empty_filename() -> None:
    generator = make_generator()

    with pytest.raises(
        ValueError,
        match="stored_filename is required",
    ):
        generator.generate(
            employee_number="QW-00002",
            document_category="passport",
            stored_filename="",
        )


def test_rejects_empty_employee_number() -> None:
    generator = make_generator()

    with pytest.raises(
        ValueError,
        match="Storage key token cannot be empty",
    ):
        generator.generate(
            employee_number="",
            document_category="passport",
            stored_filename="passport.pdf",
        )


def test_rejects_empty_document_category() -> None:
    generator = make_generator()

    with pytest.raises(
        ValueError,
        match="Storage key token cannot be empty",
    ):
        generator.generate(
            employee_number="QW-00002",
            document_category="",
            stored_filename="passport.pdf",
        )