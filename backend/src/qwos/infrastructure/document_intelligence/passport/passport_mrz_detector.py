"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    passport_mrz_detector.py

Description:
    Detects a two-line ICAO 9303 TD3 passport MRZ block from OCR text.

Responsibilities:
    - Inspect OCR text
    - Identify passport TD3 MRZ lines
    - Normalize line endings and surrounding whitespace
    - Return a clean two-line MRZ block
    - Remain independent of passport field parsing

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

import re


class PassportMRZDetectionError(ValueError):
    """
    Raised when a passport TD3 MRZ cannot be detected.
    """


class PassportMRZDetector:
    """
    Detect a two-line ICAO 9303 TD3 passport MRZ block.

    TD3 passport MRZ:
        - two lines
        - 44 characters per line
        - line 1 begins with 'P'

    The detector does not interpret individual fields or check digits.
    That responsibility belongs to PassportMRZParser.
    """

    LINE_LENGTH = 44
    LINE_COUNT = 2

    _VALID_LINE_PATTERN = re.compile(
        r"^[A-Z0-9<]{44}$",
    )

    def detect(
        self,
        ocr_text: str,
    ) -> str:
        """
        Detect and return a normalized two-line passport MRZ block.

        Raises:
            PassportMRZDetectionError:
                If no valid TD3 MRZ block can be identified.
        """

        if not ocr_text or not ocr_text.strip():
            raise PassportMRZDetectionError(
                "OCR text cannot be empty.",
            )

        lines = self._normalize_lines(
            ocr_text,
        )

        for index in range(
            len(lines) - (self.LINE_COUNT - 1),
        ):
            candidate_lines = lines[index : index + self.LINE_COUNT]

            if self._is_valid_candidate(
                candidate_lines,
            ):
                return "\n".join(
                    candidate_lines,
                )

        raise PassportMRZDetectionError(
            "Passport TD3 MRZ could not be detected in OCR text.",
        )

    def _normalize_lines(
        self,
        ocr_text: str,
    ) -> list[str]:
        """
        Normalize OCR lines for MRZ detection.

        Blank lines are removed. Surrounding whitespace is removed and all
        characters are converted to uppercase.

        Internal whitespace is removed because OCR engines may occasionally
        insert spaces into a fixed-width MRZ line.
        """

        normalized_text = ocr_text.replace("\r\n", "\n").replace("\r", "\n")

        normalized_lines: list[str] = []

        for raw_line in normalized_text.split("\n"):
            line = raw_line.strip()

            if not line:
                continue

            line = line.upper().replace(" ", "").replace("\t", "")

            normalized_lines.append(
                line,
            )

        return normalized_lines

    def _is_valid_candidate(
        self,
        lines: list[str],
    ) -> bool:
        """
        Determine whether two lines have TD3 MRZ structure.
        """

        if len(lines) != self.LINE_COUNT:
            return False

        first_line = lines[0]
        second_line = lines[1]

        if not first_line.startswith("P"):
            return False

        if not self._is_valid_mrz_line(
            first_line,
        ):
            return False

        if not self._is_valid_mrz_line(
            second_line,
        ):
            return False

        return True

    def _is_valid_mrz_line(
        self,
        line: str,
    ) -> bool:
        """
        Validate fixed-width MRZ character structure.
        """

        if len(line) != self.LINE_LENGTH:
            return False

        return bool(
            self._VALID_LINE_PATTERN.fullmatch(
                line,
            ),
        )
