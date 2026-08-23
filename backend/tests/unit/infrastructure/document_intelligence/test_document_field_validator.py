from qwos.infrastructure.document_intelligence.document_field_validator import (
    DocumentFieldValidator,
)


def test_matches_value_against_pattern() -> None:
    assert DocumentFieldValidator.matches(
        value="784-1971-4792765-7",
        validation_pattern=r"^\d{3}-\d{4}-\d{7}-\d$",
    )


def test_rejects_value_that_does_not_match_pattern() -> None:
    assert not DocumentFieldValidator.matches(
        value="784197147927657",
        validation_pattern=r"^\d{3}-\d{4}-\d{7}-\d$",
    )


def test_accepts_field_without_validation_pattern() -> None:
    assert DocumentFieldValidator.matches(
        value="Philippines",
        validation_pattern=None,
    )


def test_rejects_none_value() -> None:
    assert not DocumentFieldValidator.matches(
        value=None,
        validation_pattern=r"^\d{2}/\d{2}/\d{4}$",
    )