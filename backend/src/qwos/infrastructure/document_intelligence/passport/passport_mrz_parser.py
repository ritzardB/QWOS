"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    passport_mrz_parser.py

Description:
    Deterministic ICAO 9303 TD3 passport MRZ parser.

Responsibilities:
    - Parse two-line passport MRZ data
    - Validate MRZ structure
    - Validate ICAO check digits
    - Extract normalized passport fields
    - Produce QWOS DocumentExtraction values

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from datetime import date
from typing import Final

from qwos.application.common.ports.document_intelligence import (
    DocumentClassification,
    DocumentExtraction,
    ExtractedDocumentField,
)


class PassportMRZParseError(ValueError):
    """
    Raised when a passport MRZ cannot be parsed or validated.
    """


class PassportMRZParser:
    """
    Parse ICAO 9303 TD3 passport MRZ data.

    TD3 passports use two MRZ lines of exactly 44 characters each.

    Example structure:

        P<XXXSURNAME<<GIVEN<NAMES<<<<<<<<<<<<<<<<<<<<
        A12345678<0XXX8001011M3001019<<<<<<<<<<<<<<04

    The parser validates:
        - line lengths
        - document type
        - passport-number check digit
        - date-of-birth check digit
        - expiry-date check digit
        - composite check digit

    The parser does not perform image OCR. It expects MRZ text that has already
    been detected or supplied by an OCR/MRZ extraction component.
    """

    LINE_LENGTH: Final[int] = 44
    REQUIRED_LINE_COUNT: Final[int] = 2

    DOCUMENT_TYPE_POSITION: Final[int] = 0

    ISSUING_COUNTRY_START: Final[int] = 2
    ISSUING_COUNTRY_END: Final[int] = 5

    NAME_START: Final[int] = 5

    PASSPORT_NUMBER_START: Final[int] = 0
    PASSPORT_NUMBER_END: Final[int] = 9
    PASSPORT_NUMBER_CHECK_POSITION: Final[int] = 9

    NATIONALITY_START: Final[int] = 10
    NATIONALITY_END: Final[int] = 13

    DATE_OF_BIRTH_START: Final[int] = 13
    DATE_OF_BIRTH_END: Final[int] = 19
    DATE_OF_BIRTH_CHECK_POSITION: Final[int] = 19

    SEX_POSITION: Final[int] = 20

    EXPIRY_DATE_START: Final[int] = 21
    EXPIRY_DATE_END: Final[int] = 27
    EXPIRY_DATE_CHECK_POSITION: Final[int] = 27

    OPTIONAL_DATA_START: Final[int] = 28
    OPTIONAL_DATA_END: Final[int] = 42

    COMPOSITE_CHECK_POSITION: Final[int] = 43

    def parse(
        self,
        mrz: str,
    ) -> DocumentExtraction:
        """
        Parse and validate a TD3 passport MRZ.

        Parameters:
            mrz:
                Two-line MRZ text.

        Returns:
            DocumentExtraction containing passport classification and
            normalized extracted fields.

        Raises:
            PassportMRZParseError:
                If the supplied MRZ is malformed or fails validation.
        """

        line1, line2 = self._normalize_lines(mrz)

        self._validate_document_type(line1)

        issuing_country = self._clean(
            line1[
                self.ISSUING_COUNTRY_START : self.ISSUING_COUNTRY_END
            ],
        )

        surname, given_names = self._parse_name(
            line1[self.NAME_START :],
        )

        passport_number_raw = line2[
            self.PASSPORT_NUMBER_START : self.PASSPORT_NUMBER_END
        ]

        passport_number = self._clean(
            passport_number_raw,
        )

        passport_number_check = line2[
            self.PASSPORT_NUMBER_CHECK_POSITION
        ]

        self._validate_check_digit(
            value=passport_number_raw,
            expected_check_digit=passport_number_check,
            field_name="passport number",
        )

        nationality = self._clean(
            line2[
                self.NATIONALITY_START : self.NATIONALITY_END
            ],
        )

        date_of_birth_raw = line2[
            self.DATE_OF_BIRTH_START : self.DATE_OF_BIRTH_END
        ]

        date_of_birth_check = line2[
            self.DATE_OF_BIRTH_CHECK_POSITION
        ]

        self._validate_check_digit(
            value=date_of_birth_raw,
            expected_check_digit=date_of_birth_check,
            field_name="date of birth",
        )

        date_of_birth = self._parse_mrz_date(
            date_of_birth_raw,
            field_name="date of birth",
        )

        sex = self._parse_sex(
            line2[self.SEX_POSITION],
        )

        expiry_date_raw = line2[
            self.EXPIRY_DATE_START : self.EXPIRY_DATE_END
        ]

        expiry_date_check = line2[
            self.EXPIRY_DATE_CHECK_POSITION
        ]

        self._validate_check_digit(
            value=expiry_date_raw,
            expected_check_digit=expiry_date_check,
            field_name="expiry date",
        )

        expiry_date = self._parse_mrz_date(
            expiry_date_raw,
            field_name="expiry date",
        )

        optional_data = line2[
            self.OPTIONAL_DATA_START : self.OPTIONAL_DATA_END
        ]

        composite_data = (
            line2[
                self.PASSPORT_NUMBER_START : self.PASSPORT_NUMBER_END
            ]
            + line2[
                self.PASSPORT_NUMBER_CHECK_POSITION
            ]
            + line2[
                self.DATE_OF_BIRTH_START : self.DATE_OF_BIRTH_END
            ]
            + line2[
                self.DATE_OF_BIRTH_CHECK_POSITION
            ]
            + line2[
                self.EXPIRY_DATE_START : self.EXPIRY_DATE_END
            ]
            + line2[
                self.EXPIRY_DATE_CHECK_POSITION
            ]
            + optional_data
        )

        self._validate_check_digit(
            value=composite_data,
            expected_check_digit=line2[
                self.COMPOSITE_CHECK_POSITION
            ],
            field_name="composite passport data",
        )

        fields: list[ExtractedDocumentField] = [
            self._field(
                field_code="document_number",
                value=passport_number,
            ),
            self._field(
                field_code="surname",
                value=surname,
            ),
            self._field(
                field_code="given_names",
                value=given_names,
            ),
            self._field(
                field_code="nationality",
                value=nationality,
            ),
            self._field(
                field_code="date_of_birth",
                value=date_of_birth.isoformat(),
            ),
            self._field(
                field_code="sex",
                value=sex,
            ),
            self._field(
                field_code="expiry_date",
                value=expiry_date.isoformat(),
            ),
            self._field(
                field_code="issuing_country",
                value=issuing_country,
            ),
        ]

        return DocumentExtraction(
            classification=DocumentClassification(
                document_family="passport",
                country_code=issuing_country or None,
                confidence=1.0,
            ),
            fields=tuple(fields),
        )

    # -------------------------------------------------------------------------
    # Normalization
    # -------------------------------------------------------------------------

    def _normalize_lines(
        self,
        mrz: str,
    ) -> tuple[str, str]:
        """
        Normalize and validate the two MRZ lines.
        """

        normalized = (
            mrz.replace("\r\n", "\n")
            .replace("\r", "\n")
            .strip()
        )

        lines = [
            line.strip().upper()
            for line in normalized.split("\n")
            if line.strip()
        ]

        if len(lines) != self.REQUIRED_LINE_COUNT:
            raise PassportMRZParseError(
                "Passport TD3 MRZ must contain exactly two non-empty lines.",
            )

        for index, line in enumerate(lines, start=1):
            if len(line) != self.LINE_LENGTH:
                raise PassportMRZParseError(
                    f"Passport TD3 MRZ line {index} must contain "
                    f"{self.LINE_LENGTH} characters; got {len(line)}.",
                )

            if not all(
                character.isalnum() or character == "<"
                for character in line
            ):
                raise PassportMRZParseError(
                    f"Passport TD3 MRZ line {index} contains invalid characters.",
                )

        return lines[0], lines[1]

    # -------------------------------------------------------------------------
    # Document Type
    # -------------------------------------------------------------------------

    def _validate_document_type(
        self,
        line1: str,
    ) -> None:
        """
        Validate the TD3 passport document type.
        """

        document_type = line1[
            self.DOCUMENT_TYPE_POSITION
        ]

        if document_type != "P":
            raise PassportMRZParseError(
                "Passport TD3 MRZ must start with document type 'P'.",
            )

    # -------------------------------------------------------------------------
    # Names
    # -------------------------------------------------------------------------

    def _parse_name(
        self,
        value: str,
    ) -> tuple[str, str]:
        """
        Parse surname and given names from the TD3 name field.
        """

        parts = value.split("<<", 1)

        surname = self._clean(
            parts[0],
        )

        given_names = (
            self._clean(
                parts[1],
            )
            if len(parts) == 2
            else ""
        )

        return surname, given_names

    # -------------------------------------------------------------------------
    # Dates
    # -------------------------------------------------------------------------

    def _parse_mrz_date(
        self,
        value: str,
        *,
        field_name: str,
    ) -> date:
        """
        Parse a six-character YYMMDD MRZ date.

        MRZ dates contain a two-digit year. A rolling century rule is used:

            years 00 through 49 → 2000 through 2049
            years 50 through 99 → 1950 through 1999

        This is intentionally isolated here so the policy can be replaced
        later if QWOS introduces a more explicit date-resolution strategy.
        """

        if len(value) != 6 or not value.isdigit():
            raise PassportMRZParseError(
                f"Invalid {field_name} value in passport MRZ: {value!r}.",
            )

        year = int(value[0:2])
        month = int(value[2:4])
        day = int(value[4:6])

        full_year = (
            2000 + year
            if year <= 49
            else 1900 + year
        )

        try:
            return date(
                full_year,
                month,
                day,
            )
        except ValueError as exc:
            raise PassportMRZParseError(
                f"Invalid {field_name} date in passport MRZ: {value!r}.",
            ) from exc

    # -------------------------------------------------------------------------
    # Sex
    # -------------------------------------------------------------------------

    def _parse_sex(
        self,
        value: str,
    ) -> str | None:
        """
        Normalize the MRZ sex field.

        ICAO TD3 uses:
            M = Male
            F = Female
            < = Unspecified
        """

        if value == "M":
            return "male"

        if value == "F":
            return "female"

        if value == "<":
            return None

        raise PassportMRZParseError(
            f"Invalid passport sex value in MRZ: {value!r}.",
        )

    # -------------------------------------------------------------------------
    # Check Digits
    # -------------------------------------------------------------------------

    def _validate_check_digit(
        self,
        *,
        value: str,
        expected_check_digit: str,
        field_name: str,
    ) -> None:
        """
        Validate an ICAO 9303 MRZ check digit.
        """

        if not expected_check_digit.isdigit():
            raise PassportMRZParseError(
                f"Invalid check digit for {field_name}.",
            )

        actual_check_digit = self._calculate_check_digit(
            value,
        )

        if actual_check_digit != expected_check_digit:
            raise PassportMRZParseError(
                f"Invalid check digit for {field_name}: "
                f"expected {expected_check_digit}, "
                f"calculated {actual_check_digit}.",
            )

    def _calculate_check_digit(
        self,
        value: str,
    ) -> str:
        """
        Calculate an ICAO 9303 MRZ check digit.

        Character values:
            0-9 → numeric value
            A-Z → 10-35
            <   → 0

        Weight sequence:
            7, 3, 1 repeating
        """

        weights = (7, 3, 1)

        total = 0

        for index, character in enumerate(value):
            value_number = self._character_value(
                character,
            )

            total += (
                value_number
                * weights[index % len(weights)]
            )

        return str(total % 10)

    @staticmethod
    def _character_value(
        character: str,
    ) -> int:
        """
        Convert an MRZ character to its ICAO numeric value.
        """

        if character == "<":
            return 0

        if "0" <= character <= "9":
            return ord(character) - ord("0")

        if "A" <= character <= "Z":
            return ord(character) - ord("A") + 10

        raise PassportMRZParseError(
            f"Invalid MRZ character: {character!r}.",
        )

    # -------------------------------------------------------------------------
    # Field Construction
    # -------------------------------------------------------------------------

    @staticmethod
    def _field(
        *,
        field_code: str,
        value: str | None,
    ) -> ExtractedDocumentField:
        """
        Create a normalized extraction field.
        """

        return ExtractedDocumentField(
            field_code=field_code,
            raw_value=value,
            normalized_value=value,
            confidence=1.0,
            source="mrz",
        )

    # -------------------------------------------------------------------------
    # Text Cleaning
    # -------------------------------------------------------------------------

    @staticmethod
    def _clean(
        value: str,
    ) -> str:
        """
        Remove MRZ filler characters and normalize whitespace.
        """

        return " ".join(
            value.replace("<", " ").split(),
        )