"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

Document Intelligence

File:
    test_passport_mrz_parser.py

Description:
    Unit tests for the deterministic Passport TD3 MRZ parser.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import pytest

from qwos.infrastructure.document_intelligence.passport.passport_mrz_parser import (
    PassportMRZParseError,
    PassportMRZParser,
)

# ICAO-style TD3 specimen.
#
# The two lines must each contain exactly 44 characters.
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


def make_parser() -> PassportMRZParser:
    return PassportMRZParser()


def test_valid_mrz_fixture_has_two_44_character_lines() -> None:
    lines = VALID_MRZ.splitlines()

    assert len(lines) == 2
    assert len(lines[0]) == 44
    assert len(lines[1]) == 44


def test_parse_valid_passport_mrz() -> None:
    parser = make_parser()

    result = parser.parse(
        VALID_MRZ,
    )

    assert result.classification.document_family == (
        "passport"
    )
    assert result.classification.country_code == "UTO"
    assert result.classification.confidence == 1.0

    fields = {
        field.field_code: field
        for field in result.fields
    }

    assert fields["document_number"].normalized_value == (
        "L898902C"
    )
    assert fields["surname"].normalized_value == (
        "ERIKSSON"
    )
    assert fields["given_names"].normalized_value == (
        "ANNA MARIA"
    )
    assert fields["nationality"].normalized_value == (
        "UTO"
    )
    assert fields["date_of_birth"].normalized_value == (
        "1974-08-12"
    )
    assert fields["sex"].normalized_value == "female"
    assert fields["expiry_date"].normalized_value == (
        "2012-04-15"
    )
    assert fields["issuing_country"].normalized_value == (
        "UTO"
    )


def test_parse_accepts_crlf_input() -> None:
    parser = make_parser()

    result = parser.parse(
        VALID_MRZ.replace(
            "\n",
            "\r\n",
        ),
    )

    assert result.classification.document_family == (
        "passport"
    )


def test_parse_rejects_wrong_number_of_lines() -> None:
    parser = make_parser()

    with pytest.raises(
        PassportMRZParseError,
        match="exactly two non-empty lines",
    ):
        parser.parse(
            VALID_LINE_1,
        )


def test_parse_rejects_invalid_line_length() -> None:
    parser = make_parser()

    invalid_mrz = (
        VALID_LINE_1
        + "\n"
        + VALID_LINE_2[:-1]
    )

    with pytest.raises(
        PassportMRZParseError,
        match="must contain 44 characters",
    ):
        parser.parse(
            invalid_mrz,
        )


def test_parse_rejects_invalid_document_type() -> None:
    parser = make_parser()

    invalid_line_1 = (
        "V"
        + VALID_LINE_1[1:]
    )

    invalid_mrz = (
        invalid_line_1
        + "\n"
        + VALID_LINE_2
    )

    with pytest.raises(
        PassportMRZParseError,
        match="document type 'P'",
    ):
        parser.parse(
            invalid_mrz,
        )


def test_parse_rejects_invalid_passport_number_check_digit() -> None:
    parser = make_parser()

    invalid_line_2 = (
        VALID_LINE_2[:9]
        + "9"
        + VALID_LINE_2[10:]
    )

    invalid_mrz = (
        VALID_LINE_1
        + "\n"
        + invalid_line_2
    )

    with pytest.raises(
        PassportMRZParseError,
        match="passport number",
    ):
        parser.parse(
            invalid_mrz,
        )


def test_parse_rejects_invalid_date_of_birth_check_digit() -> None:
    parser = make_parser()

    invalid_line_2 = (
        VALID_LINE_2[:19]
        + "9"
        + VALID_LINE_2[20:]
    )

    invalid_mrz = (
        VALID_LINE_1
        + "\n"
        + invalid_line_2
    )

    with pytest.raises(
        PassportMRZParseError,
        match="date of birth",
    ):
        parser.parse(
            invalid_mrz,
        )


def test_parse_rejects_invalid_expiry_check_digit() -> None:
    parser = make_parser()

    invalid_line_2 = (
        VALID_LINE_2[:27]
        + "9"
        + VALID_LINE_2[28:]
    )

    invalid_mrz = (
        VALID_LINE_1
        + "\n"
        + invalid_line_2
    )

    with pytest.raises(
        PassportMRZParseError,
        match="expiry date",
    ):
        parser.parse(
            invalid_mrz,
        )


def test_parse_rejects_invalid_expiry_check_digit() -> None:
    parser = make_parser()

    invalid_line_2 = (
        VALID_LINE_2[:27]
        + "8"
        + VALID_LINE_2[28:]
    )

    invalid_mrz = (
        VALID_LINE_1
        + "\n"
        + invalid_line_2
    )

    with pytest.raises(
        PassportMRZParseError,
        match="expiry date",
    ):
        parser.parse(
            invalid_mrz,
        )


def test_parse_rejects_invalid_sex() -> None:
    parser = make_parser()

    invalid_line_2 = (
        VALID_LINE_2[:20]
        + "X"
        + VALID_LINE_2[21:]
    )

    invalid_mrz = (
        VALID_LINE_1
        + "\n"
        + invalid_line_2
    )

    with pytest.raises(
        PassportMRZParseError,
        match="Invalid passport sex",
    ):
        parser.parse(
            invalid_mrz,
        )