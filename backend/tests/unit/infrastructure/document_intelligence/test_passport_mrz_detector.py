"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

Document Intelligence

File:
    test_passport_mrz_detector.py

Description:
    Unit tests for PassportMRZDetector.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import pytest

from qwos.infrastructure.document_intelligence.passport.passport_mrz_detector import (
    PassportMRZDetectionError,
    PassportMRZDetector,
)

VALID_LINE_1 = (
    "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
)

VALID_LINE_2 = (
    "L898902C<3UTO7408122F1204159ZE184226B<<<<<<5"
)

VALID_MRZ = (
    f"{VALID_LINE_1}\n"
    f"{VALID_LINE_2}"
)


def make_detector() -> PassportMRZDetector:
    return PassportMRZDetector()


def test_detect_returns_valid_mrz() -> None:
    detector = make_detector()

    result = detector.detect(
        VALID_MRZ,
    )

    assert result == VALID_MRZ


def test_detect_finds_mrz_inside_other_ocr_text() -> None:
    detector = make_detector()

    ocr_text = (
        "PASSPORT\n"
        "EUROPEAN UNION\n"
        "Surname: ERIKSSON\n"
        f"{VALID_LINE_1}\n"
        f"{VALID_LINE_2}\n"
        "Some additional OCR text"
    )

    result = detector.detect(
        ocr_text,
    )

    assert result == VALID_MRZ


def test_detect_accepts_crlf_input() -> None:
    detector = make_detector()

    result = detector.detect(
        VALID_MRZ.replace(
            "\n",
            "\r\n",
        ),
    )

    assert result == VALID_MRZ


def test_detect_removes_internal_ocr_spaces() -> None:
    detector = make_detector()

    spaced_line_1 = VALID_LINE_1[:10] + " " + VALID_LINE_1[10:]
    spaced_line_2 = VALID_LINE_2[:12] + " " + VALID_LINE_2[12:]

    ocr_text = (
        f"{spaced_line_1}\n"
        f"{spaced_line_2}"
    )

    result = detector.detect(
        ocr_text,
    )

    assert result == VALID_MRZ


def test_detect_rejects_empty_text() -> None:
    detector = make_detector()

    with pytest.raises(
        PassportMRZDetectionError,
        match="cannot be empty",
    ):
        detector.detect(
            "",
        )


def test_detect_rejects_whitespace_only_text() -> None:
    detector = make_detector()

    with pytest.raises(
        PassportMRZDetectionError,
        match="cannot be empty",
    ):
        detector.detect(
            "   \n\t  ",
        )


def test_detect_rejects_missing_second_line() -> None:
    detector = make_detector()

    with pytest.raises(
        PassportMRZDetectionError,
        match="could not be detected",
    ):
        detector.detect(
            VALID_LINE_1,
        )


def test_detect_rejects_invalid_first_line_length() -> None:
    detector = make_detector()

    invalid_line_1 = VALID_LINE_1[:-1]

    with pytest.raises(
        PassportMRZDetectionError,
        match="could not be detected",
    ):
        detector.detect(
            f"{invalid_line_1}\n"
            f"{VALID_LINE_2}",
        )


def test_detect_rejects_invalid_second_line_length() -> None:
    detector = make_detector()

    invalid_line_2 = VALID_LINE_2[:-1]

    with pytest.raises(
        PassportMRZDetectionError,
        match="could not be detected",
    ):
        detector.detect(
            f"{VALID_LINE_1}\n"
            f"{invalid_line_2}",
        )


def test_detect_rejects_non_passport_document_type() -> None:
    detector = make_detector()

    invalid_line_1 = (
        "V"
        + VALID_LINE_1[1:]
    )

    with pytest.raises(
        PassportMRZDetectionError,
        match="could not be detected",
    ):
        detector.detect(
            f"{invalid_line_1}\n"
            f"{VALID_LINE_2}",
        )


def test_detect_rejects_invalid_characters() -> None:
    detector = make_detector()

    invalid_line_2 = (
        VALID_LINE_2[:20]
        + "*"
        + VALID_LINE_2[21:]
    )

    with pytest.raises(
        PassportMRZDetectionError,
        match="could not be detected",
    ):
        detector.detect(
            f"{VALID_LINE_1}\n"
            f"{invalid_line_2}",
        )


def test_detect_skips_unrelated_44_character_lines() -> None:
    detector = make_detector()

    unrelated_line = "A" * 44

    ocr_text = (
        f"{unrelated_line}\n"
        "PASSPORT\n"
        f"{VALID_LINE_1}\n"
        f"{VALID_LINE_2}"
    )

    result = detector.detect(
        ocr_text,
    )

    assert result == VALID_MRZ