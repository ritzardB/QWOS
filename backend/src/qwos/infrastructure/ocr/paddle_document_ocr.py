"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

OCR

File:
    paddle_document_ocr.py

Description:
    Local OCR implementation backed by PaddleOCR.

Responsibilities:
    - Convert image/PDF document content into OCR text
    - Keep PaddleOCR isolated from the application layer
    - Initialize the OCR engine lazily
    - Return the QWOS OCRTextResult contract

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from qwos.application.common.ports.document_ocr import (
    DocumentOCR,
    OCRTextResult,
)


class PaddleDocumentOCR(DocumentOCR):
    """
    Local OCR implementation using PaddleOCR 3.x.

    PaddleOCR is initialized lazily so the core QWOS application does not
    initialize OCR models merely because this infrastructure class is
    imported.
    """

    provider_name = "paddleocr"

    def __init__(self) -> None:
        self._ocr: Any | None = None

    def _get_ocr(self) -> Any:
        """
        Lazily initialize PaddleOCR.
        """

        if self._ocr is not None:
            return self._ocr

        try:
            from paddleocr import PaddleOCR
        except ImportError as exc:
            raise RuntimeError(
                "PaddleOCR is not installed. "
                "Install QWOS with the 'ocr' extra.",
            ) from exc

        self._ocr = PaddleOCR(
            lang="en",
        )

        return self._ocr

    def extract_text(
        self,
        *,
        content: bytes,
        filename: str,
        mime_type: str | None = None,
    ) -> OCRTextResult:
        """
        Extract OCR text from an image or PDF document.
        """

        if not content:
            raise ValueError(
                "Document content cannot be empty.",
            )

        suffix = Path(filename).suffix.lower()

        if not suffix:
            raise ValueError(
                "OCR requires a document filename with an extension.",
            )

        temporary_path: str | None = None

        try:
            with NamedTemporaryFile(
                suffix=suffix,
                delete=False,
            ) as temporary_file:
                temporary_file.write(content)
                temporary_path = temporary_file.name

            ocr = self._get_ocr()

            results = ocr.predict(
                temporary_path,
            )

            text_parts: list[str] = []

            for result in results:
                result_json = getattr(
                    result,
                    "json",
                    None,
                )

                if callable(result_json):
                    result_json = result_json()

                if not isinstance(
                    result_json,
                    dict,
                ):
                    continue

                payload = result_json.get(
                    "res",
                )

                if not isinstance(
                    payload,
                    dict,
                ):
                    continue

                recognized_text = payload.get(
                    "rec_texts",
                )

                if not isinstance(
                    recognized_text,
                    list,
                ):
                    continue

                text_parts.extend(
                    str(text)
                    for text in recognized_text
                    if text
                )

            text = "\n".join(
                text_parts,
            ).strip()

            if not text:
                raise ValueError(
                    "OCR completed but no text was detected.",
                )

            return OCRTextResult(
                text=text,
                source=self.provider_name,
                confidence=None,
            )

        finally:
            if temporary_path is not None:
                temporary_file = Path(
                    temporary_path,
                )

                if temporary_file.exists():
                    temporary_file.unlink()