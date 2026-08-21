"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

Document Intelligence

File:
    test_passport_document_intelligence.py

Description:
    Unit tests for PassportDocumentIntelligence.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from qwos.application.common.ports.document_intelligence import (
    DocumentClassification,
    DocumentExtraction,
)
from qwos.infrastructure.document_intelligence.passport.passport_document_intelligence import (
    PassportDocumentIntelligence,
)

VALID_MRZ = (
    "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\n"
    "L898902C<3UTO7408122F1204159ZE184226B<<<<<<5"
)


def make_intelligence() -> tuple[
    PassportDocumentIntelligence,
    MagicMock,
]:
    parser = MagicMock()

    parser.parse.return_value = DocumentExtraction(
        classification=DocumentClassification(
            document_family="passport",
            country_code="UTO",
            confidence=1.0,
        ),
        fields=(),
    )

    intelligence = PassportDocumentIntelligence(
        parser=parser,
    )

    return intelligence, parser


def test_classify_returns_parser_classification() -> None:
    intelligence, parser = make_intelligence()

    result = intelligence.classify(
        content=VALID_MRZ.encode(),
        filename="passport.txt",
        mime_type="text/plain",
    )

    assert result.document_family == "passport"
    assert result.country_code == "UTO"
    assert result.confidence == 1.0

    parser.parse.assert_called_once_with(
        VALID_MRZ,
    )


def test_extract_returns_parser_extraction() -> None:
    intelligence, parser = make_intelligence()

    expected = parser.parse.return_value

    result = intelligence.extract(
        content=VALID_MRZ.encode(),
        filename="passport.txt",
        mime_type="text/plain",
    )

    assert result is expected

    parser.parse.assert_called_once_with(
        VALID_MRZ,
    )


def test_extract_accepts_passport_document_family() -> None:
    intelligence, parser = make_intelligence()

    intelligence.extract(
        content=VALID_MRZ.encode(),
        filename="passport.txt",
        document_family=" passport ",
    )

    parser.parse.assert_called_once()


def test_extract_rejects_non_passport_document_family() -> None:
    intelligence, parser = make_intelligence()

    with pytest.raises(
        ValueError,
        match="only supports the passport",
    ):
        intelligence.extract(
            content=VALID_MRZ.encode(),
            filename="passport.txt",
            document_family="national_id",
        )

    parser.parse.assert_not_called()


def test_extract_rejects_country_mismatch() -> None:
    intelligence, parser = make_intelligence()

    with pytest.raises(
        ValueError,
        match="country code",
    ):
        intelligence.extract(
            content=VALID_MRZ.encode(),
            filename="passport.txt",
            country_code="PH",
        )

    parser.parse.assert_called_once()


def test_extract_accepts_matching_country_code() -> None:
    intelligence, parser = make_intelligence()

    result = intelligence.extract(
        content=VALID_MRZ.encode(),
        filename="passport.txt",
        country_code="uto",
    )

    assert result.classification.country_code == "UTO"


def test_classify_rejects_empty_content() -> None:
    intelligence, parser = make_intelligence()

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        intelligence.classify(
            content=b"",
            filename="passport.txt",
        )

    parser.parse.assert_not_called()


def test_extract_rejects_empty_content() -> None:
    intelligence, parser = make_intelligence()

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        intelligence.extract(
            content=b"",
            filename="passport.txt",
        )

    parser.parse.assert_not_called()


def test_classify_rejects_binary_content() -> None:
    intelligence, parser = make_intelligence()

    with pytest.raises(
        ValueError,
        match="Binary image/PDF OCR is not implemented yet",
    ):
        intelligence.classify(
            content=b"\xff\xd8\xff\xe0",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    parser.parse.assert_not_called()


def test_extract_rejects_binary_content() -> None:
    intelligence, parser = make_intelligence()

    with pytest.raises(
        ValueError,
        match="Binary image/PDF OCR is not implemented yet",
    ):
        intelligence.extract(
            content=b"%PDF-1.7",
            filename="passport.pdf",
            mime_type="application/pdf",
        )

    parser.parse.assert_not_called()