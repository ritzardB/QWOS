"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

OCR

File:
    paddle_document_ocr.py

Description:
    Local OCR implementation backed by PaddleOCR 3.x.

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
    Local OCR implementation using PaddleOCR.

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
                "PaddleOCR is not installed. Install QWOS with the 'ocr' extra.",
            ) from exc

        self._ocr = PaddleOCR(
            lang="en",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
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
        Extract text from an image or PDF document.
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
            confidence_values: list[float] = []

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

                recognized_scores = payload.get(
                    "rec_scores",
                )

                for index, text in enumerate(
                    recognized_text,
                ):
                    if not text:
                        continue

                    text_parts.append(
                        str(text),
                    )

                    if isinstance(
                        recognized_scores,
                        list,
                    ) and index < len(
                        recognized_scores,
                    ):
                        score = recognized_scores[index]

                        if isinstance(
                            score,
                            (int, float),
                        ):
                            confidence_values.append(
                                float(score),
                            )

            text = "\n".join(
                text_parts,
            ).strip()

            if not text:
                raise ValueError(
                    "OCR completed but no text was detected.",
                )

            confidence = sum(confidence_values) / len(confidence_values) if confidence_values else None

            return OCRTextResult(
                text=text,
                source=self.provider_name,
                confidence=confidence,
            )

        finally:
            if temporary_path is not None:
                temporary_file = Path(
                    temporary_path,
                )

                if temporary_file.exists():
                    temporary_file.unlink()
