"""
===============================================================================
Quantum Workforce OS (QWOS)

Infrastructure Layer

Document Intelligence

File:
    test_document_intelligence_router.py

Description:
    Unit tests for document-intelligence routing by document family.

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from qwos.infrastructure.document_intelligence.document_intelligence_router import (
    DocumentIntelligenceRouter,
)


def make_router() -> tuple[
    DocumentIntelligenceRouter,
    Mock,
    Mock,
]:
    passport = Mock()
    national_id = Mock()

    router = DocumentIntelligenceRouter(
        implementations={
            "passport": passport,
            "national id": national_id,
        },
    )

    return router, passport, national_id


def test_routes_passport_classification() -> None:
    router, passport, national_id = make_router()

    expected = Mock()
    passport.classify.return_value = expected

    result = router.classify(
        content=b"passport",
        filename="passport.pdf",
        mime_type="application/pdf",
        document_family="passport",
    )

    assert result is expected

    passport.classify.assert_called_once_with(
        content=b"passport",
        filename="passport.pdf",
        mime_type="application/pdf",
        document_family="passport",
    )

    national_id.classify.assert_not_called()


def test_routes_national_id_classification() -> None:
    router, passport, national_id = make_router()

    expected = Mock()
    national_id.classify.return_value = expected

    result = router.classify(
        content=b"national id",
        filename="national-id.pdf",
        mime_type="application/pdf",
        document_family="national id",
    )

    assert result is expected

    national_id.classify.assert_called_once_with(
        content=b"national id",
        filename="national-id.pdf",
        mime_type="application/pdf",
        document_family="national id",
    )

    passport.classify.assert_not_called()


def test_routes_passport_extraction() -> None:
    router, passport, national_id = make_router()

    expected = Mock()
    passport.extract.return_value = expected

    result = router.extract(
        content=b"passport",
        filename="passport.pdf",
        mime_type="application/pdf",
        document_family="passport",
        country_code="PH",
    )

    assert result is expected

    passport.extract.assert_called_once_with(
        content=b"passport",
        filename="passport.pdf",
        mime_type="application/pdf",
        document_family="passport",
        country_code="PH",
    )

    national_id.extract.assert_not_called()


def test_routes_national_id_extraction() -> None:
    router, passport, national_id = make_router()

    expected = Mock()
    national_id.extract.return_value = expected

    result = router.extract(
        content=b"national id",
        filename="national-id.pdf",
        mime_type="application/pdf",
        document_family="national id",
        country_code="AE",
    )

    assert result is expected

    national_id.extract.assert_called_once_with(
        content=b"national id",
        filename="national-id.pdf",
        mime_type="application/pdf",
        document_family="national id",
        country_code="AE",
    )

    passport.extract.assert_not_called()


def test_rejects_missing_document_family() -> None:
    router, _, _ = make_router()

    with pytest.raises(
        ValueError,
        match="Document family is required",
    ):
        router.classify(
            content=b"document",
            filename="document.pdf",
        )


def test_rejects_unsupported_document_family() -> None:
    router, _, _ = make_router()

    with pytest.raises(
        ValueError,
        match="No document intelligence implementation is registered",
    ):
        router.classify(
            content=b"document",
            filename="document.pdf",
            document_family="work permit",
        )