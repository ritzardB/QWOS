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
from qwos.application.common.ports.document_ocr import (
    OCRTextResult,
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
    MagicMock,
    MagicMock,
]:
    ocr = MagicMock()
    detector = MagicMock()
    parser = MagicMock()

    ocr.extract_text.return_value = OCRTextResult(
        text=VALID_MRZ,
        source="paddleocr",
        confidence=0.97,
    )

    detector.detect.return_value = VALID_MRZ

    parser.parse.return_value = DocumentExtraction(
        classification=DocumentClassification(
            document_family="passport",
            country_code="UTO",
            confidence=1.0,
        ),
        fields=(),
    )

    intelligence = PassportDocumentIntelligence(
        ocr=ocr,
        detector=detector,
        parser=parser,
    )

    return (
        intelligence,
        ocr,
        detector,
        parser,
    )


def test_classify_returns_parser_classification() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    result = intelligence.classify(
        content=b"passport image",
        filename="passport.jpg",
        mime_type="image/jpeg",
    )

    assert result.document_family == "passport"
    assert result.country_code == "UTO"
    assert result.confidence == 1.0

    ocr.extract_text.assert_called_once_with(
        content=b"passport image",
        filename="passport.jpg",
        mime_type="image/jpeg",
    )

    detector.detect.assert_called_once_with(
        VALID_MRZ,
    )

    parser.parse.assert_called_once_with(
        VALID_MRZ,
    )


def test_extract_returns_parser_extraction() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    expected = parser.parse.return_value

    result = intelligence.extract(
        content=b"passport image",
        filename="passport.jpg",
        mime_type="image/jpeg",
    )

    assert result is expected

    ocr.extract_text.assert_called_once_with(
        content=b"passport image",
        filename="passport.jpg",
        mime_type="image/jpeg",
    )

    detector.detect.assert_called_once_with(
        VALID_MRZ,
    )

    parser.parse.assert_called_once_with(
        VALID_MRZ,
    )


def test_extract_accepts_passport_document_family() -> None:
    (
        intelligence,
        _,
        _,
        parser,
    ) = make_intelligence()

    intelligence.extract(
        content=b"passport image",
        filename="passport.jpg",
        document_family=" passport ",
    )

    parser.parse.assert_called_once_with(
        VALID_MRZ,
    )


def test_extract_rejects_non_passport_document_family() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    with pytest.raises(
        ValueError,
        match="only supports the passport",
    ):
        intelligence.extract(
            content=b"passport image",
            filename="passport.jpg",
            document_family="national_id",
        )

    ocr.extract_text.assert_not_called()
    detector.detect.assert_not_called()
    parser.parse.assert_not_called()


def test_extract_rejects_country_mismatch() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    with pytest.raises(
        ValueError,
        match="country code",
    ):
        intelligence.extract(
            content=b"passport image",
            filename="passport.jpg",
            country_code="PH",
        )

    ocr.extract_text.assert_called_once()
    detector.detect.assert_called_once_with(
        VALID_MRZ,
    )
    parser.parse.assert_called_once_with(
        VALID_MRZ,
    )


def test_extract_accepts_matching_country_code() -> None:
    (
        intelligence,
        _,
        _,
        parser,
    ) = make_intelligence()

    result = intelligence.extract(
        content=b"passport image",
        filename="passport.jpg",
        country_code="uto",
    )

    assert result.classification.country_code == "UTO"

    parser.parse.assert_called_once_with(
        VALID_MRZ,
    )


def test_classify_rejects_empty_content() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    ocr.extract_text.side_effect = ValueError(
        "Document content cannot be empty.",
    )

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        intelligence.classify(
            content=b"",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    ocr.extract_text.assert_called_once()
    detector.detect.assert_not_called()
    parser.parse.assert_not_called()


def test_extract_rejects_empty_content() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    ocr.extract_text.side_effect = ValueError(
        "Document content cannot be empty.",
    )

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        intelligence.extract(
            content=b"",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    ocr.extract_text.assert_called_once()
    detector.detect.assert_not_called()
    parser.parse.assert_not_called()


def test_classify_propagates_ocr_failure() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    ocr.extract_text.side_effect = ValueError(
        "Binary image/PDF OCR is not implemented yet.",
    )

    with pytest.raises(
        ValueError,
        match="OCR is not implemented",
    ):
        intelligence.classify(
            content=b"passport image",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    detector.detect.assert_not_called()
    parser.parse.assert_not_called()


def test_extract_propagates_ocr_failure() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    ocr.extract_text.side_effect = ValueError(
        "Binary image/PDF OCR is not implemented yet.",
    )

    with pytest.raises(
        ValueError,
        match="OCR is not implemented",
    ):
        intelligence.extract(
            content=b"passport image",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    detector.detect.assert_not_called()
    parser.parse.assert_not_called()


def test_extract_propagates_mrz_detection_failure() -> None:
    (
        intelligence,
        ocr,
        detector,
        parser,
    ) = make_intelligence()

    detector.detect.side_effect = ValueError(
        "Passport TD3 MRZ could not be detected.",
    )

    with pytest.raises(
        ValueError,
        match="could not be detected",
    ):
        intelligence.extract(
            content=b"passport image",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    ocr.extract_text.assert_called_once()
    detector.detect.assert_called_once_with(
        VALID_MRZ,
    )
    parser.parse.assert_not_called()