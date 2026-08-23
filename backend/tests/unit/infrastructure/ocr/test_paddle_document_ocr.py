"""
===============================================================================
Quantum Workforce OS (QWOS)

Unit Tests

OCR

File:
    test_paddle_document_ocr.py

Description:
    Unit tests for PaddleDocumentOCR.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from qwos.infrastructure.ocr.paddle_document_ocr import (
    PaddleDocumentOCR,
)


def make_ocr() -> PaddleDocumentOCR:
    return PaddleDocumentOCR()


def make_paddle_result(
    *,
    recognized_text: list[str],
) -> MagicMock:
    result = MagicMock()

    result.json = {
        "res": {
            "rec_texts": recognized_text,
        },
    }

    return result


def test_constructor_does_not_initialize_paddleocr() -> None:
    with patch(
        "paddleocr.PaddleOCR",
    ) as paddle_ocr:
        ocr = make_ocr()

        paddle_ocr.assert_not_called()
        assert ocr._ocr is None


def test_extract_text_returns_ocr_result() -> None:
    ocr = make_ocr()

    fake_engine = MagicMock()

    fake_engine.predict.return_value = [
        make_paddle_result(
            recognized_text=[
                "PASSPORT",
                "ERIKSSON",
                "L898902C",
            ],
        ),
    ]

    with patch(
        "paddleocr.PaddleOCR",
        return_value=fake_engine,
    ) as paddle_ocr:
        result = ocr.extract_text(
            content=b"test document content",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    assert result.text == (
        "PASSPORT\n"
        "ERIKSSON\n"
        "L898902C"
    )
    assert result.source == "paddleocr"
    assert result.confidence is None

    paddle_ocr.assert_called_once_with(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

    fake_engine.predict.assert_called_once()


def test_extract_text_initializes_paddleocr_lazily() -> None:
    ocr = make_ocr()

    fake_engine = MagicMock()

    fake_engine.predict.return_value = [
        make_paddle_result(
            recognized_text=["PASSPORT"],
        ),
    ]

    with patch(
        "paddleocr.PaddleOCR",
        return_value=fake_engine,
    ) as paddle_ocr:
        assert ocr._ocr is None

        ocr.extract_text(
            content=b"document",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

        assert ocr._ocr is fake_engine

        ocr.extract_text(
            content=b"document",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    paddle_ocr.assert_called_once_with(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

    assert fake_engine.predict.call_count == 2


def test_extract_text_rejects_empty_content() -> None:
    ocr = make_ocr()

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        ocr.extract_text(
            content=b"",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    assert ocr._ocr is None


def test_extract_text_rejects_missing_extension() -> None:
    ocr = make_ocr()

    with pytest.raises(
        ValueError,
        match="filename with an extension",
    ):
        ocr.extract_text(
            content=b"document",
            filename="passport",
            mime_type="image/jpeg",
        )

    assert ocr._ocr is None


def test_extract_text_raises_clear_error_when_paddleocr_missing() -> None:
    ocr = make_ocr()

    with patch(
        "builtins.__import__",
        side_effect=ImportError(
            "No module named paddleocr",
        ),
    ):
        with pytest.raises(
            RuntimeError,
            match="PaddleOCR is not installed",
        ):
            ocr.extract_text(
                content=b"document",
                filename="passport.jpg",
                mime_type="image/jpeg",
            )

    assert ocr._ocr is None


def test_extract_text_rejects_when_no_text_is_detected() -> None:
    ocr = make_ocr()

    fake_engine = MagicMock()

    fake_engine.predict.return_value = [
        make_paddle_result(
            recognized_text=[],
        ),
    ]

    with patch(
        "paddleocr.PaddleOCR",
        return_value=fake_engine,
    ):
        with pytest.raises(
            ValueError,
            match="no text was detected",
        ):
            ocr.extract_text(
                content=b"document",
                filename="passport.jpg",
                mime_type="image/jpeg",
            )


def test_extract_text_ignores_results_without_expected_structure() -> None:
    ocr = make_ocr()

    valid_result = make_paddle_result(
        recognized_text=["PASSPORT"],
    )

    invalid_result = MagicMock()
    invalid_result.json = {
        "res": {},
    }

    fake_engine = MagicMock()

    fake_engine.predict.return_value = [
        invalid_result,
        valid_result,
    ]

    with patch(
        "paddleocr.PaddleOCR",
        return_value=fake_engine,
    ):
        result = ocr.extract_text(
            content=b"document",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    assert result.text == "PASSPORT"


def test_extract_text_cleans_up_temporary_file() -> None:
    ocr = make_ocr()

    fake_engine = MagicMock()

    fake_engine.predict.return_value = [
        make_paddle_result(
            recognized_text=["PASSPORT"],
        ),
    ]

    captured_path: str | None = None

    def capture_predict(
        path: str,
    ) -> list[MagicMock]:
        nonlocal captured_path

        captured_path = path

        assert Path(path).is_file()

        return fake_engine.predict.return_value

    fake_engine.predict.side_effect = capture_predict

    with patch(
        "paddleocr.PaddleOCR",
        return_value=fake_engine,
    ):
        result = ocr.extract_text(
            content=b"document",
            filename="passport.jpg",
            mime_type="image/jpeg",
        )

    assert result.text == "PASSPORT"
    assert captured_path is not None
    assert not Path(captured_path).exists()


def test_extract_text_preserves_filename_extension_case() -> None:
    ocr = make_ocr()

    fake_engine = MagicMock()

    fake_engine.predict.return_value = [
        make_paddle_result(
            recognized_text=["PASSPORT"],
        ),
    ]

    with patch(
        "paddleocr.PaddleOCR",
        return_value=fake_engine,
    ):
        result = ocr.extract_text(
            content=b"document",
            filename="passport.JPG",
            mime_type="image/jpeg",
        )

    assert result.text == "PASSPORT"
    fake_engine.predict.assert_called_once()